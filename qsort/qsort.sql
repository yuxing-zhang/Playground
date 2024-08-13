CREATE OR REPLACE FUNCTION qsort(t text) RETURNS SETOF int AS $$
DECLARE
    u int;
    b bool;
    tp text;
BEGIN
    EXECUTE format('SELECT count(*) > 0 FROM %s', t) INTO b;
    IF NOT b THEN
        RETURN;
    END IF;
    EXECUTE format('SELECT v FROM %s LIMIT 1', t) INTO u;
    LOOP
        SELECT random() INTO tp;
        EXIT WHEN NOT EXISTS (SELECT FROM pg_tables WHERE tablename = tp);
    END LOOP;
    EXECUTE format('CREATE TEMPORARY TABLE %I ON COMMIT DROP AS
                    SELECT v FROM %s WHERE v < $1', tp, t) USING u;
    RETURN QUERY SELECT * FROM qsort(format('%I', tp));
    RETURN QUERY EXECUTE format('SELECT v FROM %s WHERE v = $1', t) USING u;
    LOOP
        SELECT random() INTO tp;
        EXIT WHEN NOT EXISTS (SELECT FROM pg_tables WHERE tablename = tp);
    END LOOP;
    EXECUTE format('CREATE TEMPORARY TABLE %I ON COMMIT DROP AS
                    SELECT v FROM %s WHERE v > $1', tp, t) USING u;
    RETURN QUERY SELECT * FROM qsort(format('%I', tp));
ENd
$$ LANGUAGE plpgsql;

CREATE TABLE s(v) AS SELECT (random() * 100)::int FROM generate_series(1, 10);
TABLE s;
SELECT qsort('s');
