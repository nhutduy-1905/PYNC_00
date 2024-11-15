import psycopg2
from tkinter import *
from tkinter import messagebox

def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="student_db",
            user="postgres",
            password="123",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể kết nối đến cơ sở dữ liệu: {e}")
        return None

def register():
    def submit_registration():
        username = entry_reg_username.get()
        password = entry_reg_password.get()
        confirm_password = entry_confirm_password.get()

        if password != confirm_password:
            messagebox.showerror("Lỗi", "Mật khẩu và xác nhận mật khẩu không khớp!")
            return

        conn = connect_db()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                conn.commit()
                messagebox.showinfo("Thành công", "Đăng ký thành công! Vui lòng đăng nhập.")
                register_window.destroy()
                show_login()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Tên đăng nhập đã tồn tại hoặc lỗi khác: {e}")
            finally:
                conn.close()

    hide_all_frames()
    register_window = Frame(root)
    register_window.place(relx=0.5, rely=0.5, anchor=CENTER)

    Label(register_window, text="Đăng ký tài khoản mới", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)
    Label(register_window, text="Tên đăng nhập").grid(row=1, column=0, padx=10, pady=5)
    entry_reg_username = Entry(register_window)
    entry_reg_username.grid(row=1, column=1, padx=10, pady=5)

    Label(register_window, text="Mật khẩu").grid(row=2, column=0, padx=10, pady=5)
    entry_reg_password = Entry(register_window, show="*")
    entry_reg_password.grid(row=2, column=1, padx=10, pady=5)

    Label(register_window, text="Xác nhận mật khẩu").grid(row=3, column=0, padx=10, pady=5)
    entry_confirm_password = Entry(register_window, show="*")
    entry_confirm_password.grid(row=3, column=1, padx=10, pady=5)

    Button(register_window, text="Đăng ký", command=submit_registration).grid(row=4, column=0, columnspan=2, pady=10)
    Label(register_window, text="Đã có tài khoản?").grid(row=5, column=0, columnspan=2)
    Button(register_window, text="Đăng nhập ngay", command=lambda: [register_window.destroy(), show_login()]).grid(row=6, column=0, columnspan=2, pady=5)

def login():
    username = entry_username.get()
    password = entry_password.get()

    conn = connect_db()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cur.fetchone()
        conn.close()

        if user:
            messagebox.showinfo("Thành công", "Đăng nhập thành công!")
            show_main_menu()
        else:
            messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng!")

def show_login():
    hide_all_frames()
    login_frame = Frame(root)
    login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    Label(login_frame, text="Đăng nhập", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)
    Label(login_frame, text="Tên đăng nhập").grid(row=1, column=0, padx=10, pady=5)
    global entry_username
    entry_username = Entry(login_frame)
    entry_username.grid(row=1, column=1, padx=10, pady=5)

    Label(login_frame, text="Mật khẩu").grid(row=2, column=0, padx=10, pady=5)
    global entry_password
    entry_password = Entry(login_frame, show="*")
    entry_password.grid(row=2, column=1, padx=10, pady=5)

    Button(login_frame, text="Đăng nhập", command=login).grid(row=3, column=0, columnspan=2, pady=10)
    Label(login_frame, text="Chưa có tài khoản?").grid(row=4, column=0, columnspan=2)
    Button(login_frame, text="Đăng ký ngay", command=lambda: [login_frame.destroy(), register()]).grid(row=5, column=0, columnspan=2, pady=5)

def show_main_menu():
    hide_all_frames()
    root.title("Menu chính")

    Button(root, text="Xem dữ liệu", command=view_data, width=20).pack(pady=10)
    Button(root, text="Thêm mới", command=add_data, width=20).pack(pady=10)
    Button(root, text="Xóa dữ liệu", command=delete_data, width=20).pack(pady=10)
    Button(root, text="Cập nhật dữ liệu", command=update_data, width=20).pack(pady=10)
    Button(root, text="Đăng xuất", command=lambda: [hide_all_frames(), show_login()], width=20).pack(pady=10)

def view_data():
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM students")
        rows = cur.fetchall()
        conn.close()

        data_window = Toplevel(root)
        data_window.title("Danh sách sinh viên")

        Label(data_window, text="Danh sách sinh viên", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=4, pady=10)

        headers = ["ID", "Họ và tên", "Tuổi", "Email"]
        for col_num, header in enumerate(headers):
            Label(data_window, text=header, font=("Arial", 12, "bold")).grid(row=1, column=col_num, padx=10)

        for index, row in enumerate(rows, start=2):
            for col_num, value in enumerate(row):
                Label(data_window, text=value, font=("Arial", 12)).grid(row=index, column=col_num, padx=10)

def add_data():
    def save_data():
        name = entry_name.get()
        age = entry_age.get()
        email = entry_email.get()

        conn = connect_db()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("INSERT INTO students (name, age, email) VALUES (%s, %s, %s)", (name, age, email))
                conn.commit()
                conn.close()
                messagebox.showinfo("Thành công", "Thêm sinh viên mới thành công!")
                add_window.destroy()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể thêm sinh viên: {e}")

    add_window = Toplevel(root)
    add_window.title("Thêm sinh viên mới")

    Label(add_window, text="Họ và tên").grid(row=0, column=0, padx=10, pady=10)
    global entry_name
    entry_name = Entry(add_window)
    entry_name.grid(row=0, column=1, padx=10, pady=10)

    Label(add_window, text="Tuổi").grid(row=1, column=0, padx=10, pady=10)
    global entry_age
    entry_age = Entry(add_window)
    entry_age.grid(row=1, column=1, padx=10, pady=10)

    Label(add_window, text="Email").grid(row=2, column=0, padx=10, pady=10)
    global entry_email
    entry_email = Entry(add_window)
    entry_email.grid(row=2, column=1, padx=10, pady=10)

    Button(add_window, text="Lưu", command=save_data).grid(row=3, column=0, columnspan=2, pady=10)

def delete_data():
    def delete_by_id():
        student_id = entry_id.get()

        conn = connect_db()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM students WHERE id = %s", (student_id,))
                if cur.rowcount > 0:
                    conn.commit()
                    messagebox.showinfo("Thành công", "Xóa sinh viên thành công!")
                else:
                    messagebox.showerror("Lỗi", "Không tìm thấy sinh viên với ID này!")
                conn.close()
                delete_window.destroy()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa sinh viên: {e}")

    delete_window = Toplevel(root)
    delete_window.title("Xóa sinh viên")

    Label(delete_window, text="Nhập ID của sinh viên cần xóa").grid(row=0, column=0, padx=10, pady=10)
    global entry_id
    entry_id = Entry(delete_window)
    entry_id.grid(row=0, column=1, padx=10, pady=10)

    Button(delete_window, text="Xóa", command=delete_by_id).grid(row=1, column=0, columnspan=2, pady=10)

def update_data():
    def update_by_id():
        student_id = entry_id.get()
        new_name = entry_name.get()
        new_age = entry_age.get()
        new_email = entry_email.get()

        conn = connect_db()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    "UPDATE students SET name = %s, age = %s, email = %s WHERE id = %s",
                    (new_name, new_age, new_email, student_id)
                )
                if cur.rowcount > 0:
                    conn.commit()
                    messagebox.showinfo("Thành công", "Cập nhật thông tin thành công!")
                else:
                    messagebox.showerror("Lỗi", "Không tìm thấy sinh viên với ID này!")
                conn.close()
                update_window.destroy()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật thông tin sinh viên: {e}")

    update_window = Toplevel(root)
    update_window.title("Cập nhật thông tin sinh viên")

    Label(update_window, text="ID").grid(row=0, column=0, padx=10, pady=10)
    global entry_id
    entry_id = Entry(update_window)
    entry_id.grid(row=0, column=1, padx=10, pady=10)

    Label(update_window, text="Họ và tên mới").grid(row=1, column=0, padx=10, pady=10)
    global entry_name
    entry_name = Entry(update_window)
    entry_name.grid(row=1, column=1, padx=10, pady=10)

    Label(update_window, text="Tuổi mới").grid(row=2, column=0, padx=10, pady=10)
    global entry_age
    entry_age = Entry(update_window)
    entry_age.grid(row=2, column=1, padx=10, pady=10)

    Label(update_window, text="Email mới").grid(row=3, column=0, padx=10, pady=10)
    global entry_email
    entry_email = Entry(update_window)
    entry_email.grid(row=3, column=1, padx=10, pady=10)

    Button(update_window, text="Cập nhật", command=update_by_id).grid(row=4, column=0, columnspan=2, pady=10)

def hide_all_frames():
    for widget in root.winfo_children():
        widget.destroy()

root = Tk()
root.title("Ứng dụng quản lý sinh viên")
root.geometry("800x600")
show_login()
root.mainloop()
