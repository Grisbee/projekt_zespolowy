CREATE TABLE products (
    product_id VARCHAR(10) PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price NUMERIC(10,2),
    url TEXT,
    product_source VARCHAR(10),
    currency VARCHAR(3)
);

CREATE TABLE categories (
    category_id VARCHAR(20) PRIMARY KEY,
    category_name TEXT
);

CREATE TABLE price_history (
    history_id VARCHAR(15) PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(product_id) ON DELETE CASCADE,
    price NUMERIC(10, 2) NOT NULL
);

CREATE TABLE product_categories (
    product_id VARCHAR(20) NOT NULL REFERENCES products(product_id) ON DELETE CASCADE,
    category_id VARCHAR(20) NOT NULL REFERENCES categories(category_id) ON DELETE CASCADE,
    PRIMARY KEY (product_id, category_id)
);