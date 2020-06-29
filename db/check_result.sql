create table check_result (
    id                  uuid            PRIMARY KEY,
    created 		    bigint          not null, 
    url                 TEXT            not null,
    status              int             not null,
    response_time_ms    bigint          not null
);

create index check_result_created_idx           on check_result (created);
create index check_result_url_idx               on check_result (url);
create index check_result_status_idx            on check_result (status);
