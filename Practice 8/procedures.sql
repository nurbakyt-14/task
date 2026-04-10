
-- 1. UPSERT procedure (update if exists, insert if not)
CREATE OR REPLACE PROCEDURE upsert_contact(
    p_name VARCHAR,
    p_surname VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN

    IF EXISTS (SELECT 1 FROM contacts WHERE phone = p_phone) THEN
        UPDATE contacts 
        SET name = p_name, 
            surname = p_surname, 
            updated_at = CURRENT_TIMESTAMP
        WHERE phone = p_phone;
        RAISE NOTICE 'Contact updated (phone existed): % %', p_name, p_surname;
    
    ELSIF EXISTS (SELECT 1 FROM contacts WHERE name = p_name AND surname = p_surname) THEN
        UPDATE contacts 
        SET phone = p_phone, 
            updated_at = CURRENT_TIMESTAMP
        WHERE name = p_name AND surname = p_surname;
        RAISE NOTICE 'Phone updated for: % %', p_name, p_surname;
    
    ELSE
        INSERT INTO contacts (name, surname, phone, created_at, updated_at) 
        VALUES (p_name, p_surname, p_phone, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
        RAISE NOTICE 'New contact added: % %', p_name, p_surname;
    END IF;
    
EXCEPTION
    WHEN unique_violation THEN
        RAISE NOTICE 'Duplicate phone detected, updating instead...';
        UPDATE contacts 
        SET name = p_name, 
            surname = p_surname, 
            updated_at = CURRENT_TIMESTAMP
        WHERE phone = p_phone;
END;
$$;

 

-- 2. Type for storing invalid records
DROP TYPE IF EXISTS invalid_record CASCADE;
CREATE TYPE invalid_record AS (
    name VARCHAR,
    surname VARCHAR,
    phone VARCHAR,
    error_message VARCHAR
);


-- 3. Insert many contacts procedure
CREATE OR REPLACE PROCEDURE insert_many_contacts(
    contacts_data TEXT[][],
    INOUT invalid_records invalid_record[] DEFAULT '{}'
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INTEGER;
    phone_valid BOOLEAN;
    contact_name VARCHAR;
    contact_surname VARCHAR;
    contact_phone VARCHAR;
BEGIN
    FOR i IN 1..array_length(contacts_data, 1)
    LOOP
        contact_name := contacts_data[i][1];
        contact_surname := contacts_data[i][2];
        contact_phone := contacts_data[i][3];
    
        -- Validate phone number (10-15 digits, optional + prefix)
        phone_valid := contact_phone ~ '^\+?[0-9]{10,15}$';
        
        IF phone_valid THEN
            CALL upsert_contacts(contact_name, contact_surname, contact_phone);
        
                              
        ELSE
            invalid_records := invalid_records || 
                ROW(contact_name, contact_surname, contact_phone, 
                    'Invalid phone number! Format: +7XXXXXXXXX or 8XXXXXXXXXX')::invalid_record;
        END IF;
    END LOOP;
    
    RAISE NOTICE 'Added/updated: % records, Failed: % records', 
        array_length(contacts_data, 1) - array_length(invalid_records, 1),
        array_length(invalid_records, 1);
END;
$$;

-- 4. Delete contact procedure
CREATE OR REPLACE PROCEDURE delete_contact(
    p_name VARCHAR DEFAULT NULL,
    p_surname VARCHAR DEFAULT NULL,
    p_phone VARCHAR DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    IF p_phone IS NOT NULL THEN
        DELETE FROM contacts WHERE phone = p_phone;
        
        GET DIAGNOSTICS deleted_count = ROW_COUNT;
        RAISE NOTICE 'Deleted % record(s) by phone', deleted_count;
        
    ELSIF p_name IS NOT NULL AND p_surname IS NOT NULL THEN
        DELETE FROM contacts WHERE name = p_name AND surname = p_surname;
        GET DIAGNOSTICS deleted_count = ROW_COUNT;
        RAISE NOTICE 'Deleted % record(s) by name (% %)', deleted_count, p_name, p_surname;
        
    ELSIF p_name IS NOT NULL THEN
        DELETE FROM contacts WHERE name = p_name;
        GET DIAGNOSTICS deleted_count = ROW_COUNT;
        RAISE NOTICE 'Deleted % record(s) by name (%)', deleted_count, p_name;
        
    ELSE
        RAISE EXCEPTION 'Error: At least one parameter (name, surname, or phone) must be provided';
    END IF;
END;
$$;

-- 5. Clear all contacts procedure
CREATE OR REPLACE PROCEDURE clear_all_contacts()
LANGUAGE plpgsql
AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO deleted_count FROM contacts;
    DELETE FROM contacts;
    RAISE NOTICE 'Deleted all % contacts', deleted_count;
END;
$$;