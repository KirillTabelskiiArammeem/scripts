kratos new helpdesk-facade -r git@gitlab.zeus.arammeem.net:platform/go/kratos-layout.git

kratos proto add api/application/helpdesk.proto

kratos proto client api/application/helpdesk.proto

kratos proto client api/application/error_reason.proto

kratos proto server api/application/helpdesk.proto -t internal/service

kratos proto client api/application/record.proto

