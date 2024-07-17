
CREATE TABLE if not exists <<DB_TABLE_NAME>> (
        pk TEXT DEFAULT format('guid#%s',uuid_generate_v4 ()),
        sk TEXT not null check (length(sk) < 500),
        tk TEXT DEFAULT format('guid#%s',uuid_generate_v4 ()),
        form jsonb not null,
        active BOOLEAN NOT NULL DEFAULT true,
        created timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
        updated timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
        owner TEXT
      );
      CREATE UNIQUE INDEX IF NOT EXISTS one_first_idx ON <<DB_TABLE_NAME>>(pk,sk);
      CREATE INDEX IF NOT EXISTS one_second_idx ON <<DB_TABLE_NAME>>(sk,tk);
      /* speed up resource query by bounding rect */
      CREATE INDEX IF NOT EXISTS one_second_flip_idx ON <<DB_TABLE_NAME>>(tk, sk);