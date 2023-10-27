CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create users table
CREATE TABLE IF NOT EXISTS users(
    user_id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    email TEXT,
    password TEXT,
    date TEXT,
    requests_count INT
);

-- Create chats table
CREATE TABLE IF NOT EXISTS chats(
    chat_id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(user_id),
    creation_time TIMESTAMP DEFAULT current_timestamp,
    chat_name TEXT
);

-- Create api_keys table
CREATE TABLE IF NOT EXISTS api_keys(
    key_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(user_id),
    api_key TEXT UNIQUE,
    creation_time TIMESTAMP DEFAULT current_timestamp,
    deleted_time TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

--- Create prompts table
CREATE TABLE IF NOT EXISTS prompts (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    title VARCHAR(255),
    content TEXT,
    status VARCHAR(255) DEFAULT 'private'
);

--- Create brains table
CREATE TABLE IF NOT EXISTS brains (
  brain_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT NOT NULL,
  status TEXT,
  description TEXT,
  prompt_id UUID REFERENCES prompts(id),
  linkedin TEXT,
  extraversion INT,
  neuroticism INT,
  conscientiousness INT
);

-- Create brains_data table
CREATE TABLE IF NOT EXISTS brains_data (
  brain_id UUID,
  data_sha1 TEXT,
  metadata JSONB,
  PRIMARY KEY (brain_id, data_sha1),
  FOREIGN KEY (brain_id) REFERENCES brains (brain_id)
);

-- Create chat_history table
CREATE TABLE IF NOT EXISTS chat_history (
    message_id UUID DEFAULT uuid_generate_v4(),
    chat_id UUID REFERENCES chats(chat_id),
    brain_id UUID REFERENCES brains(brain_id),
    user_message TEXT,
    assistant TEXT,
    message_time TIMESTAMP DEFAULT current_timestamp,
    PRIMARY KEY (chat_id, message_id)
);

-- Create brains X users table
CREATE TABLE IF NOT EXISTS brains_users (
  brain_id UUID REFERENCES brains (brain_id),
  user_id UUID REFERENCES users (user_id),
  rights VARCHAR(255),
  default_brain BOOLEAN DEFAULT false,
  PRIMARY KEY (brain_id, user_id)
);

-- Create brains subscription invitations table
CREATE TABLE IF NOT EXISTS brain_subscription_invitations (
  brain_id UUID,
  email VARCHAR(255),
  rights VARCHAR(255),
  PRIMARY KEY (brain_id, email),
  FOREIGN KEY (brain_id) REFERENCES brains (brain_id)
);

CREATE OR REPLACE FUNCTION public.get_user_email_by_user_id(user_id uuid)
RETURNS TABLE (email text)
SECURITY definer
AS $$
BEGIN
  RETURN QUERY SELECT users.email::text FROM users WHERE users.id = user_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION public.get_user_id_by_user_email(user_email text)
RETURNS TABLE (user_id uuid)
SECURITY DEFINER
AS $$
BEGIN
  RETURN QUERY SELECT users.id::uuid FROM users WHERE users.email = user_email;
END;
$$ LANGUAGE plpgsql;

