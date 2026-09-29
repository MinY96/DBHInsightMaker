-- 1. 기본 테이블 생성 (파티션 테이블 선언)
CREATE TABLE IF NOT EXISTS public.user_logs (
    event_time VARCHAR(12) NOT NULL,
    user_id VARCHAR(25),
    main_cat_id VARCHAR(15),
    sub_cat_id VARCHAR(30),
    counts INTEGER,
    CONSTRAINT user_logs_pk PRIMARY KEY (event_time, user_id, main_cat_id, sub_cat_id)
) PARTITION BY RANGE (event_time);

-- 2026년 02월 파티션 생성 (From 은 포함, To는 미포함)
CREATE TABLE IF NOT EXISTS public.user_logs_202602 PARTITION OF public.user_logs
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');

-- 2026년 03월 파티션 생성
CREATE TABLE IF NOT EXISTS public.user_logs_202603 PARTITION OF public.user_logs
    FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');

-- 2026년 04월 파티션 생성
CREATE TABLE IF NOT EXISTS public.user_logs_202604 PARTITION OF public.user_logs
    FOR VALUES FROM ('2026-04-01') TO ('2026-05-01');

-- 2026년 05월 파티션 생성
CREATE TABLE IF NOT EXISTS public.user_logs_202605 PARTITION OF public.user_logs
    FOR VALUES FROM ('2026-05-01') TO ('2026-06-01');

-- 2026년 06월 파티션 생성
CREATE TABLE IF NOT EXISTS public.user_logs_202606 PARTITION OF public.user_logs
    FOR VALUES FROM ('2026-06-01') TO ('2026-07-01');

-- 2026년 07월 파티션 생성
CREATE TABLE IF NOT EXISTS public.user_logs_202607 PARTITION OF public.user_logs
    FOR VALUES FROM ('2026-07-01') TO ('2026-08-01');

-- 2026년 08월 파티션 생성
CREATE TABLE IF NOT EXISTS public.user_logs_202608 PARTITION OF public.user_logs
    FOR VALUES FROM ('2026-08-01') TO ('2026-09-01');

-- 2026년 09월 파티션 생성
CREATE TABLE IF NOT EXISTS public.user_logs_202609 PARTITION OF public.user_logs
    FOR VALUES FROM ('2026-09-01') TO ('2026-10-01');

-- 2026년 10월 파티션 생성
CREATE TABLE IF NOT EXISTS public.user_logs_202610 PARTITION OF public.user_logs
    FOR VALUES FROM ('2026-10-01') TO ('2026-11-01');

-- 2026년 11월 파티션 생성
CREATE TABLE IF NOT EXISTS public.user_logs_202611 PARTITION OF public.user_logs
    FOR VALUES FROM ('2026-11-01') TO ('2026-12-01');

-- 2026년 12월 파티션 생성
CREATE TABLE IF NOT EXISTS public.user_logs_202612 PARTITION OF public.user_logs
    FOR VALUES FROM ('2026-12-01') TO ('2027-01-01');