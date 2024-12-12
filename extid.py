x = """message

bad query: DELETE FROM ir_attachment WHERE id IN (4599296, 4599295) ERROR: could not serialize access due to concurrent delete

bad query: DELETE FROM ir_attachment WHERE id IN (4611070) ERROR: could not serialize access due to concurrent delete

bad query: DELETE FROM ir_attachment WHERE id IN (4611070) ERROR: could not serialize access due to concurrent delete

bad query: DELETE FROM ir_attachment WHERE id IN (4611043) ERROR: could not serialize access due to concurrent delete

bad query: DELETE FROM ir_attachment WHERE id IN (4611043) ERROR: could not serialize access due to concurrent delete

bad query: DELETE FROM ir_attachment WHERE id IN (4611024) ERROR: could not serialize access due to concurrent delete

bad query: DELETE FROM ir_attachment WHERE id IN (4611004) ERROR: could not serialize access due to concurrent delete

bad query: DELETE FROM ir_attachment WHERE id IN (4611004) ERROR: could not serialize access due to concurrent delete

bad query: DELETE FROM ir_attachment WHERE id IN (4610984) ERROR: could not serialize access due to concurrent delete

bad query: DELETE FROM ir_attachment WHERE id IN (4610984) ERROR: could not serialize access due to concurrent delete

bad query: DELETE FROM ir_attachment WHERE id IN (4610965) ERROR: could not serialize access due to concurrent delete

bad query: DELETE FROM ir_attachment WHERE id IN (4610937) ERROR: could not serialize access due to concurrent delete

bad query: DELETE FROM ir_attachment WHERE id IN (4610937) ERROR: could not serialize access due to concurrent delete

bad query: DELETE FROM ir_attachment WHERE id IN (4610926, 4610876) ERROR: could not serialize access due to concurrent delete

bad query: DELETE FROM ir_attachment WHERE id IN (4610917) ERROR: could not serialize access due to concurrent delete

bad query: DELETE FROM ir_attachment WHERE id IN (4610917) ERROR: could not serialize access due to concurrent delete

bad query: DELETE FROM ir_attachment WHERE id IN (4610898) ERROR: could not serialize access due to concurrent delete

bad query: DELETE FROM ir_attachment WHERE id IN (4610871) ERROR: could not serialize access due to concurrent delete

bad query: DELETE FROM ir_attachment WHERE id IN (4610871) ERROR: could not serialize access due to concurrent delete

bad query: DELETE FROM ir_attachment WHERE id IN (4610851) ERROR: could not serialize access due to concurrent delete

bad query: DELETE FROM ir_attachment WHERE id IN (4610851) ERROR: could not serialize access due to concurrent delete

bad query: DELETE FROM ir_attachment WHERE id IN (4610822) ERROR: could not serialize access due to concurrent delete

bad query: DELETE FROM ir_attachment WHERE id IN (4610812) ERROR: could not serialize access due to concurrent delete

bad query: DELETE FROM ir_attachment WHERE id IN (4610802) ERROR: could not serialize access due to concurrent delete

bad query: DELETE FROM ir_attachment WHERE id IN (4610792) ERROR: could not serialize access due to concurrent delete

bad query: DELETE FROM ir_attachment WHERE id IN (4610782) ERROR: could not serialize access due to concurrent delete

bad query: DELETE FROM ir_attachment WHERE id IN (4610772) ERROR: could not serialize access due to concurrent delete

bad query: DELETE FROM ir_attachment WHERE id IN (4610762) ERROR: could not serialize access due to concurrent delete

bad query: DELETE FROM ir_attachment WHERE id IN (4610752) ERROR: could not serialize access due to concurrent delete

bad query: DELETE FROM ir_attachment WHERE id IN (4610742) ERROR: could not serialize access due to concurrent delete

bad query: DELETE FROM ir_attachment WHERE id IN (4610731) ERROR: could not serialize access due to concurrent delete

bad query: DELETE FROM ir_attachment WHERE id IN (4610719) ERROR: could not serialize access due to concurrent delete

bad query: DELETE FROM ir_attachment WHERE id IN (4599261) ERROR: could not serialize access due to concurrent delete

bad query: DELETE FROM ir_attachment WHERE id IN (4607406, 4607405, 4607404, 4607403, 4599255, 4599254) ERROR: could not serialize access due to concurrent delete"""

import re

nums = re.findall('\d+', x)
print(tuple(int(n) for n in nums))