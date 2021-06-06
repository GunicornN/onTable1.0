-- MUST BE RUNNED IN onTable DATABASE
-- this script will create a trigger needed for the python print server to work

-- Add entry in company_printstatus for the Tornado bot
CREATE OR REPLACE FUNCTION notify_new_cart() RETURNS trigger AS $$ 
BEGIN 
	INSERT INTO company_printstatus (cart_id_id, status, created_on) VALUES (NEW.id, 0, current_timestamp) ON CONFLICT DO NOTHING;
    RETURN NEW; 
END; 
$$ LANGUAGE plpgsql;

-- Notify the Tornado bot when an UPDATE or INSERT is executed in printstatus table
CREATE OR REPLACE FUNCTION company_printstatus_update() RETURNS trigger AS $$
BEGIN
	-- this will execute a postgres function that'll trigger an eventwith the pk of added element in payload
    -- this'll allow the python script to know which element has been added
	IF (NEW.status <> 1) THEN
		PERFORM pg_notify('company_cart_insert_event', ''|| NEW.cart_id_id);
	END IF;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Delete existing trigger before overwriting it
DROP TRIGGER IF EXISTS insert_company_cart ON company_cart;
CREATE TRIGGER insert_company_cart AFTER INSERT OR UPDATE ON company_cart FOR EACH ROW EXECUTE FUNCTION notify_new_cart();

DROP TRIGGER IF EXISTS update_printstatus ON company_printstatus;
CREATE TRIGGER update_printstatus AFTER INSERT OR UPDATE ON company_printstatus FOR EACH ROW EXECUTE FUNCTION company_printstatus_update();