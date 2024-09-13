import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime


class DatabaseManager:
    def __init__(self, db_file) -> None:
        self.db_file = db_file

    def _connect(self):
        return sqlite3.connect(self.db_file)

    def query(self, query, params=()):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def execute(self, query, params=()):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

    def add_product(
        self, sku, description, id_department, id_class, id_family, stock,
        quantity, record_delete, model, brand, record_data, discontinued
    ):
        query = """
        INSERT OR IGNORE INTO Product (
            sku, description, id_department, id_class, id_family, stock,
            quantity, record_delete, model, brand, record_data, discontinued
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(query, (
            sku, description, id_department, id_class, id_family, stock,
            quantity, record_delete, model, brand, record_data, discontinued
        ))

    def update_product(
        self, sku, description, id_department, id_class, id_family, stock,
        quantity, record_delete, model, brand, record_data, discontinued
    ):
        query = """
        UPDATE Product
        SET description = ?, id_department = ?, id_class = ?, id_family = ?,
        stock = ?, quantity = ?, record_delete = ?, model = ?, brand = ?,
        record_data = ?, discontinued = ?
        WHERE sku = ?
        """
        self.execute(query, (
            description, id_department, id_class, id_family, stock,
            quantity, record_delete, model, brand, record_data, discontinued, 
            sku))

    def delete_product(self, sku):
        query = "DELETE FROM Product WHERE sku = ?"
        self.execute(query, (sku,))

    def get_product_by_sku(self, sku):
        query = """
        SELECT p.sku, p.description, p.id_department, p.id_class, p.id_family,
            p.brand, p.model, p.stock, p.quantity, p.discontinued,
            p.record_delete, p.record_data,
            d.name AS department_name,
            c.name AS class_name,
            f.name AS family_name
        FROM Product p
        JOIN Department d ON p.id_department = d.id
        JOIN Class c ON p.id_class = c.id AND p.id_department = c.id_department
        JOIN Family f ON p.id_family = f.id AND p.id_class = f.id_class
        AND p.id_department = f.id_department
        WHERE p.sku = ?
        """
        return self.query(query, (sku,))

    def generate_hierarchical_data(self):
        department_dict = {}
        class_dict = {}
        family_dict = {}

        # Obtener la lista de departamentos
        departments = self.query("SELECT id, name FROM Department")

        # Para cada departamento, obtener sus clases
        for dept_id, dept_name in departments:
            department_dict[dept_name] = dept_id
            classes = self.query(
                "SELECT id, name FROM Class WHERE id_department = ?",
                (dept_id,)
                )
            class_dict[dept_id] = {
                class_name: class_id for class_id, class_name in classes
            }

            # Para cada clase, obtener sus familias
            for class_id, class_name in classes:
                families = self.query(
                    "SELECT id, name FROM Family WHERE id_department = ? AND id_class = ?",
                    (dept_id, class_id)
                )
                family_dict[(dept_id, class_id)] = {
                    family_name: family_id for family_id,
                    family_name in families}

        return department_dict, class_dict, family_dict


class ProductApp:
    def __init__(self, root, db_file):
        self.db_manager = DatabaseManager(db_file)

        self.department_dict, self.class_dict, self.family_dict = (
            self.db_manager.generate_hierarchical_data())

        self.root = root
        self.root.title("Gestión de Productos")

        # Define width for all Entry and ComboBox widgets
        field_width = 30

        # Create Labels and Entries
        validate_sku = root.register(self.validate_sku_key)
        validate_text = root.register(self.validate_text_key)
        validate_stock = root.register(self.validate_stock_key)
        validate_quantity = root.register(self.validate_quantity_key)

        tk.Label(root, text="SKU:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.sku_entry = tk.Entry(
            root, width=field_width, validate="key", validatecommand=(validate_sku, '%S', '%P'))
        self.sku_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(root, text="Descripción:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.description_entry = tk.Entry(
            root, width=field_width, validate="key",
            validatecommand=(validate_text, '%S', '%P', 15))
        self.description_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(root, text="Marca:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.brand_entry = tk.Entry(
            root, width=field_width, validate="key",
            validatecommand=(validate_text, '%S', '%P', 15))
        self.brand_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(root, text="Modelo:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.model_entry = tk.Entry(
            root, width=field_width, validate="key",
            validatecommand=(validate_text, '%S', '%P', 20))
        self.model_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(root, text="Departamento:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.department_combobox = ttk.Combobox(root, state=tk.DISABLED, width=field_width)
        self.department_combobox.grid(row=4, column=1, padx=10, pady=5)
        self.department_combobox.config(values=list(self.department_dict.keys()))
        self.department_combobox.bind("<<ComboboxSelected>>", self.update_classes)

        tk.Label(root, text="Clase:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.class_combobox = ttk.Combobox(root, state=tk.DISABLED, width=field_width)
        self.class_combobox.grid(row=5, column=1, padx=10, pady=5)
        self.class_combobox.bind("<<ComboboxSelected>>", self.update_families)

        tk.Label(root, text="Familia:").grid(row=6, column=0, padx=10, pady=5, sticky="e")
        self.family_combobox = ttk.Combobox(root, state=tk.DISABLED, width=field_width)
        self.family_combobox.grid(row=6, column=1, padx=10, pady=5)

        tk.Label(root, text="Stock:").grid(row=7, column=0, padx=10, pady=5, sticky="e")
        self.stock_entry = tk.Entry(root, width=field_width,
            validate="key", validatecommand=(validate_stock, '%S', '%P'))
        self.stock_entry.grid(row=7, column=1, padx=10, pady=5)

        tk.Label(root, text="Cantidad:").grid(row=8, column=0, padx=10, pady=5, sticky="e")
        self.quantity_entry = tk.Entry(
            root, width=field_width, validate="key", validatecommand=(validate_quantity, '%S', '%P'))
        self.quantity_entry.grid(row=8, column=1, padx=10, pady=5)

        tk.Label(root, text="Fecha de Registro:").grid(row=9, column=0, padx=10, pady=5, sticky="e")
        self.record_data_entry = tk.Entry(root, width=field_width, state=tk.DISABLED)
        self.record_data_entry.grid(row=9, column=1, padx=10, pady=5)

        tk.Label(root, text="Fecha de Baja:").grid(row=10, column=0, padx=10, pady=5, sticky="e")
        self.record_delete_entry = tk.Entry(root, width=field_width, state=tk.DISABLED)
        self.record_delete_entry.grid(row=10, column=1, padx=10, pady=5)

        self.discontinued_var = tk.BooleanVar()
        self.discontinued_checkbutton = tk.Checkbutton(
            root, text="Descontinuado",
            variable=self.discontinued_var,
            state=tk.NORMAL
        )
        self.discontinued_checkbutton.config(state=tk.DISABLED)
        self.discontinued_checkbutton.grid(
            row=11, column=0, columnspan=2, padx=10, pady=5
        )

        self.msg_lbl = tk.Label(root, text="").grid(row=12, column=0, padx=10, pady=5, sticky="e")

        # Create Buttons
        self.consult_button = tk.Button(root, text="Consultar", command=self.consult_product, state=tk.DISABLED)
        self.consult_button.grid(row=1, column=3, padx=10, pady=5)
        self.add_button = tk.Button(root, text="Agregar", command=self.add_or_update_product, state=tk.DISABLED)
        self.add_button.grid(row=2, column=3, padx=10, pady=5)
        self.edit_button = tk.Button(root, text="Editar", command=self.edit_form, state=tk.DISABLED)
        self.edit_button.grid(row=3, column=3, padx=10, pady=5)
        self.delete_button = tk.Button(root, text="Eliminar", command=self.delete_product, state=tk.DISABLED)
        self.delete_button.grid(row=5, column=3, padx=10, pady=5)
        self.clean_button = tk.Button(root, text="Limpiar", command=self.clear_form, state=tk.DISABLED)
        self.clean_button.grid(row=4, column=3, padx=10, pady=5)

        # Initialize date fields with current date
        self.clear_form()

    def update_classes(self, event=None):
        department = self.department_combobox.get()
        department_id = self.department_dict.get(department)
        if department_id:
            classes = list(self.class_dict.get(department_id, {}).keys())
            self.class_combobox.config(values=classes)
            self.class_combobox.set(classes[0])

    def update_families(self, event=None):
        department = self.department_combobox.get()
        department_id = self.department_dict.get(department)
        class_name = self.class_combobox.get()
        if department_id and class_name:
            class_id = self.class_dict.get(department_id, {}).get(class_name)
            families = list(self.family_dict.get((department_id, class_id), {}).keys()) if class_id else []
            self.family_combobox.config(values=families)
            self.family_combobox.set(families[0])

    def edit_form(self):
        self.toogle_form_fields(True)
        self.add_button.config(text="Actualizar")
        self.delete_button.config(state=tk.DISABLED)

    def disable_form(self):
        self.description_entry.config(state=tk.DISABLED)
        self.brand_entry.config(state=tk.DISABLED)
        self.model_entry.config(state=tk.DISABLED)
        self.department_combobox.config(state=tk.DISABLED)
        self.class_combobox.config(state=tk.DISABLED)
        self.family_combobox.config(state=tk.DISABLED)
        self.stock_entry.config(state=tk.DISABLED)
        self.quantity_entry.config(state=tk.DISABLED)

        self.add_button.config(state=tk.DISABLED)
        self.clean_button.config(state=tk.DISABLED)
        self.delete_button.config(state=tk.DISABLED)
        self.consult_button.config(state=tk.DISABLED)
        self.edit_button.config(state=tk.DISABLED)

    def full_activate_form(self):
        self.description_entry.config(state=tk.NORMAL)
        self.brand_entry.config(state=tk.NORMAL)
        self.model_entry.config(state=tk.NORMAL)
        self.department_combobox.config(state=tk.NORMAL)
        self.class_combobox.config(state=tk.NORMAL)
        self.family_combobox.config(state=tk.NORMAL)
        self.stock_entry.config(state=tk.NORMAL)
        self.quantity_entry.config(state=tk.NORMAL)

        self.add_button.config(state=tk.NORMAL)
        self.clean_button.config(state=tk.NORMAL)
        self.delete_button.config(state=tk.NORMAL)
        self.consult_button.config(state=tk.NORMAL)
        self.edit_button.config(state=tk.NORMAL)

    def toogle_form_fields(self, status: bool):
        entry_st = tk.NORMAL if status else tk.DISABLED

        self.description_entry.config(state=entry_st)
        self.brand_entry.config(state=entry_st)
        self.model_entry.config(state=entry_st)
        self.department_combobox.config(state=entry_st)
        self.class_combobox.config(state=entry_st)
        self.family_combobox.config(state=entry_st)
        self.stock_entry.config(state=entry_st)
        self.quantity_entry.config(state=entry_st)
        self.discontinued_checkbutton.config(state=entry_st)
        self.add_button.config(state=entry_st)

    def set_current_dates(self):
        today = datetime.now().strftime("%Y-%m-%d")

        self.record_data_entry.config(state=tk.NORMAL)
        self.record_data_entry.delete(0, tk.END)
        self.record_data_entry.insert(0, today)
        self.record_data_entry.config(state="readonly")

        self.record_delete_entry.config(state=tk.NORMAL)
        self.record_delete_entry.delete(0, tk.END)
        self.record_delete_entry.insert(0, '1900-01-01')
        self.record_delete_entry.config(state="readonly")

    def clear_form(self):
        # Habilitar todos los campos antes de limpiarlos
        self.full_activate_form()

        # Borrar el contenido de los campos
        self.sku_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.brand_entry.delete(0, tk.END)
        self.model_entry.delete(0, tk.END)
        self.stock_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)

        # Restablecer valores predeterminados en los combobox y el checkbutton
        self.department_combobox.set("")
        self.class_combobox.set("")
        self.family_combobox.set("")
        self.discontinued_var.set(False)

        self.add_button.config(text="Agregar")

        # Restablecer las fechas actuales en los campos de fecha
        today = datetime.now().strftime("%Y-%m-%d")
        self.record_data_entry.delete(0, tk.END)
        self.record_data_entry.insert(0, today)
        self.record_delete_entry.delete(0, tk.END)
        self.record_delete_entry.insert(0, '1900-01-01')

        # Deshabilitar los campos nuevamente después de limpiarlos
        self.disable_form()

    def consult_product(self):
        sku = self.sku_entry.get()
        result = self.db_manager.get_product_by_sku(sku)

        if result:
            self.fill_form(result)
            self.edit_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)
            self.clean_button.config(state=tk.NORMAL)
        else:
            self.toogle_form_fields(True)
            self.edit_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)
            self.clean_button.config(state=tk.NORMAL)

    def fill_form(self, data):
        product_info = data[0]

        print(product_info)

        self.update_data_form(self.description_entry, product_info[1])
        self.update_data_form(self.brand_entry, product_info[5])
        self.update_data_form(self.model_entry, product_info[6])
        self.update_data_form(self.stock_entry, product_info[7])
        self.update_data_form(self.quantity_entry, product_info[8])
        self.update_data_form(self.record_delete_entry, product_info[10])
        self.update_data_form(self.record_data_entry, product_info[11])

        try:
            self.department_combobox.current(product_info[2] - 1)
            self.update_classes()

            self.class_combobox.current(product_info[3] - 1)
            self.update_families()

            self.family_combobox.current(product_info[4] - 1)
        except IndexError as e:
            print(f"IndexError: {e}. Verifica que 'product_info' tenga suficientes elementos.")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def update_data_form(self, field, value):
        field.config(state=tk.NORMAL)
        field.delete(0, tk.END)
        if value is None:
            field.insert(0, '')
        else:
            field.insert(0, value)
        field.config(state=tk.DISABLED)
        print(value)

    def show_msg(self, field):
        messagebox.showwarning(
            "Información faltante",
            field
        )

    def add_or_update_product(self):
        sku = self.sku_entry.get()
        description = self.description_entry.get().strip()
        model = self.model_entry.get().strip()
        id_department = self.department_combobox.current() + 1
        id_class = self.class_combobox.current() + 1
        id_family = self.family_combobox.current() + 1
        stock = self.stock_entry.get()
        quantity = self.quantity_entry.get()
        brand = self.brand_entry.get().strip()
        record_data = self.record_data_entry.get().strip()
        record_delete = self.record_delete_entry.get().strip()
        discontinued = self.discontinued_var.get()

        if sku == '':
            self.show_msg('SKU')
            return None

        if description == '':
            self.show_msg('Artículo')
            return None

        if brand == '':
            self.show_msg('Marca')
            return None

        if model == '':
            self.show_msg('Modelo')
            return None

        if self.department_combobox.current() == -1:
            self.show_msg('Departamento')
            return None

        if self.class_combobox.current() == -1:
            self.show_msg('Clase')
            return None

        if self.family_combobox.current() == -1:
            self.show_msg('Familia')
            return None

        if stock == '':
            self.show_msg('Stock')
            return None

        if quantity == '':
            self.show_msg('Cantidad')
            return None

        if description == '':
            self.show_msg('Artículo')
            return None

        action = self.add_button.cget('text')

        if discontinued:
            today = datetime.now().strftime("%Y-%m-%d")
            record_delete = today

        if action == 'Agregar':
            self.db_manager.add_product(
                sku, description, id_department, id_class, id_family, stock,
                quantity, record_delete, model, brand, record_data, discontinued
            )
        else:
            self.db_manager.update_product(
                sku, description, id_department, id_class, id_family, stock,
                quantity, record_delete, model, brand, record_data, discontinued
            )

        self.add_button.config(text="Agregar", state=tk.DISABLED)
        self.disable_form()

        print(self.db_manager.get_product_by_sku(sku))

    def delete_product(self):
        result = messagebox.askyesno(
            "Confirmar Eliminación",
            "¿Estás seguro de que deseas eliminar este registro?"
        )
        if result:
            sku = self.sku_entry.get()
            self.db_manager.delete_product(sku)
            self.clear_form()
        else:
            pass

    def validate_sku_key(self, char, entry_value):
        if char.isdigit() and len(entry_value) <= 6:
            self.update_consult_button(entry_value)
            return True
        elif char == "":
            self.update_consult_button(entry_value[:-1])
            return True
        return False

    def validate_stock_key(self, char, entry_value):
        if char.isdigit() and len(entry_value) <= 9:
            return True
        elif char == "":
            return True
        return False

    def validate_quantity_key(self, char, entry_value):
        limit = int(self.stock_entry.get())
        current = int(entry_value) if entry_value != "" else 0

        if char.isdigit() and len(entry_value) <= 9 and limit >= current:
            return True
        elif char == "":
            return True
        return False

    def validate_text_key(self, char, entry_value, max_length):
        if char.isalpha() or char == "":
            if len(entry_value) < int(max_length):
                return True
            else:
                return False
        return False

    def update_consult_button(self, entry_value):
        if 0 < len(entry_value) <= 6:
            self.consult_button.config(state=tk.NORMAL)
        else:
            self.consult_button.config(state=tk.DISABLED)
            self.toogle_form_fields(False)


if __name__ == "__main__":
    root = tk.Tk()
    app = ProductApp(root, "data.db")
    root.mainloop()
