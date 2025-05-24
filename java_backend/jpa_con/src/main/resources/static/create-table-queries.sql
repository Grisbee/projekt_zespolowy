-- Rozszerzenie UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Istniejące tabele
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price NUMERIC(10,2),
    url TEXT,
    product_source VARCHAR(10),
    currency VARCHAR(3),
    rating NUMERIC(2,1),
    review_count INTEGER
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

-- Nowe tabele z diagramu
CREATE TABLE Product (
    keepa_name VARCHAR(255) PRIMARY KEY,
    amazon_title TEXT,
    link_keepa TEXT,
    link_amazon TEXT,
    chart_url TEXT,
    price_box INTEGER,
    price_new INTEGER,
    price_used INTEGER,
    product_category VARCHAR(255),
    rating VARCHAR(10),
    review_count VARCHAR(20),
    currency VARCHAR(3),
    product_src VARCHAR(50)
);

CREATE TABLE SimilarProducts (
    id VARCHAR(255) PRIMARY KEY,
    similar_product_1 VARCHAR(255) REFERENCES Product(keepa_name) ON DELETE SET NULL,
    similar_product_2 VARCHAR(255) REFERENCES Product(keepa_name) ON DELETE SET NULL,
    similar_product_3 VARCHAR(255) REFERENCES Product(keepa_name) ON DELETE SET NULL,
    similar_product_4 VARCHAR(255) REFERENCES Product(keepa_name) ON DELETE SET NULL
);

-- Indeksy dla lepszej wydajności
CREATE INDEX idx_similar_products_1 ON SimilarProducts(similar_product_1);
CREATE INDEX idx_similar_products_2 ON SimilarProducts(similar_product_2);
CREATE INDEX idx_similar_products_3 ON SimilarProducts(similar_product_3);
CREATE INDEX idx_similar_products_4 ON SimilarProducts(similar_product_4);