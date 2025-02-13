queue.job.function(339, 350, 361, 372, 383, 394, 405, 416, 429, 436, 450, 460)

jobs = env["queue.job.function"].search([])
names = set(jobs.mapped("name"))

for name in names:
    jobs = env["queue.job.function"].search([("name", "=", name)])
    if len(jobs) > 1:
        print(name)
        mj = max(jobs, key=lambda j: j.id)
        to_delete = jobs - mj
        to_delete.unlink()
        env.cr.commit()
