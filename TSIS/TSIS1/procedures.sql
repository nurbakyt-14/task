-- Procedure 1: add_phone
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    -- Find contact by name
    SELECT id INTO v_contact_id FROM contacts WHERE name = p_contact_name;
    
    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found', p_contact_name;
    END IF;
    
    -- Add phone
    INSERT INTO phones (contact_id, phone, type) 
    VALUES (v_contact_id, p_phone, p_type);
    
    RAISE NOTICE 'Phone % added to contact %', p_phone, p_contact_name;
END;
$$;

-- Procedure 2: move_to_group
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_group_id INTEGER;
    v_contact_id INTEGER;
BEGIN
    -- Get or create group
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
    
    IF v_group_id IS NULL THEN
        INSERT INTO groups (name) VALUES (p_group_name) RETURNING id INTO v_group_id;
        RAISE NOTICE 'Created new group: %', p_group_name;
    END IF;
    
    -- Update contact's group
    UPDATE contacts 
    SET group_id = v_group_id 
    WHERE name = p_contact_name
    RETURNING id INTO v_contact_id;
    
    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found', p_contact_name;
    END IF;
    
    RAISE NOTICE 'Contact % moved to group %', p_contact_name, p_group_name;
END;
$$;

-- Function 3: search_contacts (extended)
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    name VARCHAR(100),
    phone TEXT,
    email VARCHAR(100),
    birthday DATE,
    group_name VARCHAR(50)
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        c.name,
        string_agg(DISTINCT p.phone || '(' || p.type || ')', ', ') as phones,
        c.email,
        c.birthday,
        g.name as group_name
    FROM contacts c
    LEFT JOIN phones p ON c.id = p.contact_id
    LEFT JOIN groups g ON c.group_id = g.id
    WHERE 
        c.name ILIKE '%' || p_query || '%'
        OR c.email ILIKE '%' || p_query || '%'
        OR p.phone ILIKE '%' || p_query || '%'
        OR g.name ILIKE '%' || p_query || '%'
    GROUP BY c.id, c.name, c.email, c.birthday, g.name;
END;
$$;