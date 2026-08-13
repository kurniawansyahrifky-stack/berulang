from telethon import types

class Inline:
    @staticmethod
    def dashboard_menu():
        btn_primary = types.KeyboardButtonStyle(bg_primary=True, icon=6138780272088322672)
        btn_danger = types.KeyboardButtonStyle(bg_danger=True, icon=6084880262179588505)
        return [
            [types.KeyboardButtonCallback(text="⚙️ Kelola Multi-Pesan", data=b"manage_tasks", style=btn_primary)],
            [types.KeyboardButtonCallback(text="➕ Buat Pesan Baru", data=b"create_task", style=btn_primary)],
            [types.KeyboardButtonCallback(text="📋 Bantuan / Help", data=b"help_menu", style=btn_primary)],
            [types.KeyboardButtonCallback(text="❌ Tutup Menu", data=b"close_panel", style=btn_danger)]
        ]

    @staticmethod
    def help_menu():
        btn_primary = types.KeyboardButtonStyle(bg_primary=True)
        return [
            [types.KeyboardButtonUrl(text="🛍️ MY STORE", url="https://t.me/storegarf", style=btn_primary)],
            [types.KeyboardButtonCallback(text="🔙 Kembali", data=b"menu_main", style=types.KeyboardButtonStyle(bg_danger=True))]
        ]

    @staticmethod
    def task_list_menu(tasks):
        buttons = []
        btn_primary = types.KeyboardButtonStyle(bg_primary=True)
        btn_danger = types.KeyboardButtonStyle(bg_danger=True)
        
        for t in tasks:
            buttons.append([
                types.KeyboardButtonCallback(text=f"✏️ Edit #{t['id']}", data=f"edit_task_{t['id']}".encode('utf-8'), style=btn_primary),
                types.KeyboardButtonCallback(text=f"🗑️ Hapus #{t['id']}", data=f"del_task_{t['id']}".encode('utf-8'), style=btn_danger)
            ])
        buttons.append([types.KeyboardButtonCallback(text="➕ Tambah Pesan Baru", data=b"create_task", style=btn_primary)])
        buttons.append([types.KeyboardButtonCallback(text="🔙 Kembali", data=b"menu_main", style=types.KeyboardButtonStyle(bg_danger=True))])
        return buttons

    @staticmethod
    def cancel_menu(callback_data=b"manage_tasks"):
        btn_danger = types.KeyboardButtonStyle(bg_danger=True)
        return [[types.KeyboardButtonCallback(text="❌ Batal", data=callback_data, style=btn_danger)]]

    @staticmethod
    def interval_menu():
        btn_primary = types.KeyboardButtonStyle(bg_primary=True)
        return [
            [
                types.KeyboardButtonCallback(text="⏱️ 5 Mnt", data=b"inter_m_5", style=btn_primary),
                types.KeyboardButtonCallback(text="⏱️ 15 Mnt", data=b"inter_m_15", style=btn_primary),
                types.KeyboardButtonCallback(text="⏱️ 30 Mnt", data=b"inter_m_30", style=btn_primary)
            ],
            [
                types.KeyboardButtonCallback(text="⏳ 1 Jam", data=b"inter_h_1", style=btn_primary),
                types.KeyboardButtonCallback(text="⏳ 2 Jam", data=b"inter_h_2", style=btn_primary),
                types.KeyboardButtonCallback(text="⏳ 5 Jam", data=b"inter_h_5", style=btn_primary)
            ]
        ]

    @staticmethod
    def hours_menu():
        btns = []
        row = []
        btn_primary = types.KeyboardButtonStyle(bg_primary=True)
        for h in range(24):
            row.append(types.KeyboardButtonCallback(text=f"{h:02d}:00", data=f"hour_{h}".encode('utf-8'), style=btn_primary))
            if len(row) == 4:
                btns.append(row)
                row = []
        if row:
            btns.append(row)
        return btns
