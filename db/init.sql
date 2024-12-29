DO
$$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'app_db') THEN
        CREATE DATABASE app_db;
    END IF;
END
$$;
