import uuid
users_ext_id = ['__export__.res_users_a_durrani_ruh', '__export__.res_users_a_fahd_jed', '__export__.res_users_a_karumedukkil_ruh', '__export__.res_users_f_khurshaid_ruh', '__export__.res_users_j_alsaadi_jed', '__export__.res_users_m_omar', '__export__.res_users_m_nouman_jed', '__export__.res_users_m_raza_ruh', '__export__.res_users_n_alenezi', '__export__.res_users_n_alabdullah', '__export__.res_users_y_abbas_jed', '__export__.res_users_y_abusamra', '__export__.res_users_r_alnahar']

query_tmpl = """
UPDATE ir_model_data
SET name = '{}'
WHERE name = '{}'
"""

for user_ext_id in users_ext_id:
    user = env.ref(user_ext_id)
    user_id = user.id
    name = f"res_users_{user_id}_{uuid.uuid4().hex[:8]}"
    query = query_tmpl.format(name, user_ext_id.split('.')[1])
    print(query)

