# translation.py

import os

CONFIG_FILE = 'config.txt'

def load_language_setting():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            for line in file:
                if line.startswith('language='):
                    return line.strip().split('=')[1]
    return 'english'

def translate(text):
    language = load_language_setting()
    translations = {
        #main menu
        "Menu": {"english": "Menu", "bahasa": "Menu"},
        "Random Item Picker": {"english": "Random Item Picker", "bahasa": "Pilih Item Acak"},
        "Group Generator": {"english": "Group Generator", "bahasa": "Generator Kelompok"},
        "Tournament Bracket Generator": {"english": "Tournament Bracket Generator", "bahasa": "Generator Braket Turnamen"},
        "Coloring Generator": {"english": "Coloring Generator", "bahasa": "Generator Pewarnaan Gambar"},
        "Card Generator": {"english": "Card Generator", "bahasa": "Generator Kartu"},
        "Dice Generator": {"english": "Dice Generator", "bahasa": "Generator Dadu"},
        "Coin Generator": {"english": "Coin Generator", "bahasa": "Generator Koin"},
        "Random Number Generator": {"english": "Random Number Generator", "bahasa": "Generator Angka Acak"},
        "Random Maze Generator": {"english": "Random Maze Generator", "bahasa": "Generator Labirin Acak"},
        "Random Color Generator": {"english": "Random Color Generator", "bahasa": "Generator Warna Acak"},
        "Random Password Generator": {"english": "Random Password Generator", "bahasa": "Generator Kata Sandi Acak"},
        "Random Coordinate Generator": {"english": "Random Coordinate Generator", "bahasa": "Generator Koordinat Acak"},
        "Tools": {"english": "Tools", "bahasa": "Alat"},
        "Import": {"english": "Import", "bahasa": "Impor"},
        "Change Language": {"english": "Change Language to Bahasa", "bahasa": "Change Language to English"},
        "Help": {"english": "Help", "bahasa": "Bantuan"},
        "User Guide": {"english": "User Guide", "bahasa": "Panduan Pengguna"},
        "About": {"english": "About", "bahasa": "Tentang"},
        #modul
        "Enter team names below (one per line):":{"english": "Enter team names below (one per line):", "bahasa": "Masukkan nama tim (satu nama per baris):"},
        "Generate Bracket":{"english": "Generate Bracket", "bahasa": "Generate Braket"},
        "Minimum of two names required.":{"english": "Minimum of two names required.", "bahasa": "Harap masukkan setidaknya 2 nama"},
        "Save Bracket":{"english": "Save Bracket", "bahasa": "Simpan Braket"},
        "error_minimum_teams":{"english": "Please enter at least 2 team names.", "bahasa": "Harap masukkan setidaknya 2 nama tim."},
        "Pick Random Item": {"english": "Pick Random Item", "bahasa": "Pilih Item Acak"},
        "Enter items below (one per line):":{"english": "Enter items below (one per line):", "bahasa": "Masukkan nama item (satu per baris)"},
        "Remove Picked Item":{"english": "Remove Picked Item", "bahasa": "Hapus item yang terpilih"},
        "Please enter at least one item.":{"english": "Please enter at least one item.", "bahasa": "Harap setidaknya mengisi satu item"},
        "Randomly picked item:\n": {"english": "Randomly picked item:\n", "bahasa": "Item yang dipilih secara acak:\n"},
        "Enter names below (one per line):":{"english": "Enter names below (one per line):", "bahasa": "masukkan nama (satu per baris)"},
        "Select number of groups:":{"english": "Select number of groups:", "bahasa": "Pilih Jumlah Grup"},
        "Generate Groups":{"english": "Generate Groups", "bahasa": "Generate Grup"},
        "Save Group Image":{"english": "Save Group Image", "bahasa": "Simpan Gambar Grup"},
        "error_minimum_names":{"english": "Please enter at least 2 names.", "bahasa": "Harus setidaknya mengisi dua nama"},
        "Choose Image":{"english": "Choose Image", "bahasa": "Pilih Gambar"},
        "Save Image":{"english": "Save Image", "bahasa": "Simpan Gambar"},
        "Generate Random Card":{"english": "Generate Random Card", "bahasa": "Generate kartu acak"},
        "Roll Dice": {"english": "Roll Dice", "bahasa": "Kocok Dadu"},
        "Roll 1 Die": {"english": "Roll 1 Die", "bahasa": "Kocok 1 Dadu"},
        "Roll 2 Dice": {"english": "Roll 2 Dice", "bahasa": "Kocok 2 Dadu"},
        "Coin Flipper":{"english": "Coin Flipper", "bahasa": "Pemutar Koin"},
        "Flip Coin": {"english": "Flip Coin", "bahasa": "Putar Koin"},
        "Number Set Generator":{"english": "Number Set Generator", "bahasa": "Generator Set Angka"},
        "Number of Digits:":{"english": "Number of Digits:", "bahasa": "Jumlah Digit:"},
        "Number of Sets:":{"english": "Number of Sets:", "bahasa": "Jumlah Set:"},
        "Generate Sets":{"english": "Generate Sets", "bahasa": "Generate Set Angka"},
        "Maze Generator":{"english": "Maze Generator", "bahasa": "Generator Labirin"},
        "Width:":{"english": "Width:", "bahasa": "Lebar:"},
        "Height:":{"english": "Height:", "bahasa": "Tinggi:"},
        "Generate Maze":{"english": "Generate Maze", "bahasa": "Generate Labirin"},
        "Save Maze":{"english": "Save Maze", "bahasa": "Simpan Gambar Labirin"},
        "Random Color Picker":{"english": "Random Color Picker", "bahasa": "Pemilih Warna Acak"},
        "Pick Random Color":{"english": "Pick Random Color", "bahasa": "Pilih Warna Acak"},
        "Copy Color":{"english": "Copy Color", "bahasa": "Salin Warna"},
        "Password Length:":{"english": "Password Length:", "bahasa": "Panjang Kata Sandi"},
        "Generate Password":{"english": "Generate Password", "bahasa": "Generate Kata Sandi"},    
        "Copy Password":{"english": "Copy Password", "bahasa": "Salin Kata Sandi"},
        "Latitude Range:":{"english": "Latitude Range:", "bahasa": "Rentang Garis Lintang"},
        "Longitude Range:":{"english": "Longitude Range:", "bahasa": "Rentang Garis Bujur"},
        "Number of Coordinates:":{"english": "Number of Coordinates:", "bahasa": "Jumlah Koordinat"},
        "Generate Coordinates":{"english": "Generate Coordinates", "bahasa": "Generate Koordinat"},
        "Copy Coordinates":{"english": "Copy Coordinates", "bahasa": "Salin Koordinat"},
        "You can find the location on a coordinate converter":{"english": "You can find the location on a coordinate converter", "bahasa": "Lokasi dapat dicari menggunakan konverter koordinat"},
        "enter_valid_numbers": {"english": "Please enter valid numbers for digit count and number of sets.", "bahasa": "Silahkan masukkan angka yang valid untuk jumlah digit dan jumlah set."},
        "copied": {"english": "Color copied to clipboard!", "bahasa": "Warna disalin ke clipboard!"},
        "error_password": {"english": "Please enter a valid number for password length", "bahasa": "Silahkan masukkan nomor yang valid untuk panjang password"},
        "password_copied": {"english": "Password copied to clipboard!", "bahasa": "kata sandi disalin ke clipboard!"},
        "coor_copied": {"english": "Coordinate copied to clipboard!", "bahasa": "Koordinat disalin ke clipboard!"},
        "coor_error": {"english": "Latitude must be between -90 and 90, and longitude must be between -180 and 180.", "bahasa": "Garis lintang harus antara -90 dan 90, dan garis bujur harus antara -180 dan 180."},
        "coordinate_info": {"english": "Coordinate {idx}: (Latitude: {latitude:.6f}, Longitude: {longitude:.6f})\n","bahasa": "Koordinat {idx}: (Lintang: {latitude:.6f}, Bujur: {longitude:.6f})\n"},
        "guide_text": {"bahasa": "Panduan Pengguna:\n\n1. Pilih Item Acak:\n- Pilih opsi 'Pilih Item Acak' dari menu 'Menu'.\n- Masukkan item yang ingin di-random, satu per baris.\n- Klik 'Generate' untuk mendapatkan item acak.\n\n2. Generator Kelompok:\n- Pilih opsi 'Generator Kelompok' dari menu 'Menu'.\n- Masukkan nama anggota yang ingin dikelompokkan.\n- Tentukan jumlah grup atau biarkan 'auto' untuk pengelompokan otomatis.\n- Klik 'Generate' untuk menghasilkan grup.\n\n3. Generator Braket Turnamen:\n- Pilih opsi 'Generator Braket Turnamen' dari menu 'Menu'.\n- Masukkan tim yang berpartisipasi.\n- Klik 'Generate' untuk membuat braket turnamen.\n\n4. Generator Pewarnaan Gambar:\n- Pilih opsi 'Generator Pewarnaan Gambar' dari menu 'Menu'.\n- Klik 'Pilih Gambar' untuk memberi pola pewarnaan acak pada gambar tersebut.\n\n5. Generator Kartu:\n- Pilih opsi 'Generator Kartu' dari menu 'Menu'.\n- Klik 'Generate' untuk menghasilkan kartu acak.\n\n6. Generator Dadu:\n- Pilih opsi 'Generator Dadu' dari menu 'Menu'.\n- Tentukan jumlah dadu yang ingin dilempar.\n- Klik 'Generate' untuk melempar dadu dan melihat hasilnya.\n\n7. Generator koin:\n- Pilih opsi 'Generator Koin' dari menu 'Menu'.\n- Klik 'Generate' untuk melempar koin dan melihat hasilnya (Head atau Tail).\n\n8. Generator Angka Acak:\n- Pilih opsi 'Generator Angka Acak' dari menu 'Menu'.\n- Tentukan jumlah digit dan set yang ingin dihasilkan.\n- Klik 'Generate' untuk menghasilkan angka acak.\n\n9. Generator Labirin Acak:\n- Pilih opsi 'Generator Labirin Acak' dari menu 'Menu'.\n- Klik 'Generate' untuk membuat labirin acak.\n\n10.Generator Warna Acak:\n- Pilih opsi 'Generator Warna Acak' dari menu 'Menu'.\n- Klik 'Generate' untuk memilih warna acak.\n\n11.Generator kata Sandi Acak:\n- Pilih opsi 'Generator Kata Sandi Acak' dari menu 'Menu'.\n- Tentukan panjang password.\n- Klik 'Generate' untuk menghasilkan password acak.\n\n12.Generator Koordinat Acak:\n- Pilih opsi 'Generator Koordinat Acak' dari menu 'Menu'.\n- Klik 'Generate' untuk mendapatkan koordinat acak.","english": "User Guide:\n\n1. Random Item Picker:\n- Select the 'Random Item Picker' option from the 'Menu'.\n- Enter the items you want to randomize, one per line.\n- Click 'Generate' to get a random item.\n\n2. Group Generator:\n- Select the 'Group Generator' option from the 'Menu'.\n- Enter the names of the members you want to group.\n- Specify the number of groups or leave it at 'auto' for automatic grouping.\n- Click 'Generate' to create groups.\n\n3. Tournament Bracket Generator:\n- Select the 'Tournament Bracket Generator' option from the 'Menu'.\n- Enter the participating teams.\n- Click 'Generate' to create the tournament bracket.\n\n4. Coloring Generator:\n- Select the 'Coloring Generator' option from the 'Menu'.\n- Click 'Choose Image' to Apply a random coloring pattern to the image.\n\n5. Card Generator:\n- Select the 'Card Generator' option from the 'Menu'.\n- Click 'Generate' to generate random cards.\n\n6. Dice Generator:\n- Select the 'Dice Generator' option from the 'Menu'.\n- Specify the number of dice you want to roll.\n- Click 'Generate' to roll the dice and see the result.\n\n7. Coin Generator:\n- Select the 'Coin Generator' option from the 'Menu'.\n- Click 'Generate' to flip a coin and see the result (Heads or Tails).\n\n8. Random Number Generator:\n- Select the 'Random Number Generator' option from the 'Menu'.\n- Specify the digit count and the number of sets to generate.\n- Click 'Generate' to create random numbers.\n\n9. Random Maze Generator:\n- Select the 'Random Maze Generator' option from the 'Menu'.\n- Click 'Generate' to create a random maze.\n\n10. Random Color Generator:\n- Select the 'Random Color Generator' option from the 'Menu'.\n- Click 'Generate' to pick a random color.\n\n11. Random Password Generator:\n- Select the 'Random Password Generator' option from the 'Menu'.\n- Specify the password length.\n- Click 'Generate' to create a random password.\n\n12. Random Coordinate Generator:\n- Select the 'Random Coordinate Generator' option from the 'Menu'.\n- Click 'Generate' to get a random coordinate."},
        "faq_text":{"english": "Frequently Asked Questions:\n\nQ: How do I change the application language?\nA: Select 'Change Language' from the 'Tools' menu. The application will switch between English and Indonesian.\n\nQ: How do I import data from a file?\nA: Select 'Import' from the 'Tools' menu. Choose the file you want to import (txt, xlsx, docx). The data will be inserted into the active tool. However, it can only be imported into the Random Item Picker, Group Generator, and Tournament Bracket Generator menus.\n\nQ: What should I do if I find a bug?\nA: Contact the application developer or send a report through the 'About' feature.","bahasa":"Frequently Asked Questions:\n\nQ: Bagaimana cara mengubah bahasa aplikasi?\nA: Pilih 'Ganti Bahasa' dari menu 'Alat'. Aplikasi akan berganti antara bahasa Inggris dan Bahasa Indonesia.\n\nQ: Bagaimana cara mengimpor data dari file?\nA: Pilih 'Impor' dari menu 'Alat'. Pilih file yang ingin diimpor (txt, xlsx, docx). Data akan dimasukkan ke alat yang sedang aktif. Namun hanya dapat diimpor ke menu Pilih Item Acak, Generator Kelompok, dan Generator Braket Turnamen.\n\nQ: Apa yang harus dilakukan jika saya menemukan bug?\nA: Hubungi pengembang aplikasi atau kirim laporan melalui fitur 'Tentang'."}
  }
    
    return translations.get(text, {}).get(language, text)
