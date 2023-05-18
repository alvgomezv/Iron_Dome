
import magic

file_magic = magic.Magic()

file_type = file_magic.from_file('./hola')
print(file_type)