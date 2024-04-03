vault login -method=token $(vault write -field=token ${VAULT_JWT_LOGIN_PATH} role=${VAULT_ROLE} jwt=$(cat /run/secrets/kubernetes.io/serviceaccount/token))

vault kv patch -mount="bss" "${VAULT_NAMESPACE}/applications" deploy.toggle.install.app=True
vault kv patch -mount="bss" "${VAULT_NAMESPACE}/applications" deploy.toggle.update.app=True
vault kv patch -mount="bss" "${VAULT_NAMESPACE}/applications" deploy.modules_to_update="aram_base"
vault kv patch -mount="bss" "${VAULT_NAMESPACE}/applications" deploy.modules_to_install="aram_vault"
vault kv patch -mount="bss" "${VAULT_NAMESPACE}/applications" deploy.toggle.reset.jobs=True
vault kv patch -mount="bss" "${VAULT_NAMESPACE}/applications" deploy.toggle.working.kafka_consumers=True


vault kv patch -mount="bss" "${VAULT_NAMESPACE}/applications" deploy.status.working_kafka_consumer.RepportalApplicant.process_app=True
vault kv patch -mount="bss" "${VAULT_NAMESPACE}/applications" deploy.status.working_kafka_consumer.RepportalApplicantFiles.process_app_files=True
vault kv patch -mount="bss" "${VAULT_NAMESPACE}/applications" deploy.status.working_kafka_consumer.RepportalFleetCompany.process_company=True
vault kv patch -mount="bss" "${VAULT_NAMESPACE}/applications" deploy.status.working_kafka_consumer.RepportalKPIStatitstic.process_kpi_statistic=True
vault kv patch -mount="bss" "${VAULT_NAMESPACE}/applications" deploy.status.working_kafka_consumer.RepportalReferralLinks.process_referral_link=True
vault kv patch -mount="bss" "${VAULT_NAMESPACE}/applications" deploy.status.working_kafka_consumer.RepportalRepresentative.process_rep=True
vault kv patch -mount="bss" "${VAULT_NAMESPACE}/applications" deploy.status.working_kafka_consumer.DriverLocation.process_driver_location=True

