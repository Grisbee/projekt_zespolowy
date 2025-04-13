CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price NUMERIC(10,2),
    url TEXT,
    product_source VARCHAR(10),
    currency VARCHAR(3),
    rating NUMERIC(2,1),
    review_count INTEGER,
    img_url TEXT
);

CREATE TABLE categories (
    category_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    category_name TEXT
);

CREATE TABLE price_history (
    history_id VARCHAR(15) PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(product_id) ON DELETE CASCADE,
    price NUMERIC(10, 2) NOT NULL
);

CREATE TABLE product_categories (
    product_id INTEGER NOT NULL REFERENCES products(product_id) ON DELETE CASCADE,
    category_id UUID NOT NULL REFERENCES categories(category_id) ON DELETE CASCADE,
    PRIMARY KEY (product_id, category_id)
);
