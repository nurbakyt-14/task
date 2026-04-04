
-- 1. Search function (by name, surname, or phone)
CREATE OR REPLACE FUNCTION search_contacts(search_pattern VARCHAR)
RETURNS TABLE(
    id INTEGER,
    name VARCHAR,
    surname VARCHAR,
    phone VARCHAR
) 
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.name, c.surname, c.phone
    FROM contacts c
    WHERE c.name ILIKE '%' || search_pattern || '%'
       OR c.surname ILIKE '%' || search_pattern || '%'
       OR c.phone ILIKE '%' || search_pattern || '%'
    ORDER BY c.surname, c.name;
END;
$$;

-- 2. Pagination function
CREATE OR REPLACE FUNCTION get_contacts_paginated(
    p_page_num INTEGER,
    p_page_size INTEGER
)
RETURNS TABLE(
    id INTEGER,
    name VARCHAR,
    surname VARCHAR,
    phone VARCHAR,
    total_count BIGINT
)
LANGUAGE plpgsql
AS $$
DECLARE
    offset_val INTEGER;
BEGIN
    offset_val := (p_page_num - 1) * p_page_size;
    
    RETURN QUERY
    SELECT c.id, c.name, c.surname, c.phone,
           (SELECT COUNT(*) FROM contacts) AS total_count
    FROM contacts c
    ORDER BY c.surname, c.name
    LIMIT p_page_size OFFSET offset_val;
END;
$$;

-- 3. Get all contacts function
CREATE OR REPLACE FUNCTION get_all_contacts()
RETURNS TABLE(
    id INTEGER,
    name VARCHAR,
    surname VARCHAR,
    phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.name, c.surname, c.phone
    FROM contacts c
    ORDER BY c.surname, c.name;
END;
$$;

-- 4. Find contact by phone function
CREATE OR REPLACE FUNCTION find_by_phone(p_phone VARCHAR)
RETURNS TABLE(
    id INTEGER,
    name VARCHAR,
    surname VARCHAR,
    phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.name, c.surname, c.phone
    FROM contacts c
    WHERE c.phone = p_phone;
END;
$$;