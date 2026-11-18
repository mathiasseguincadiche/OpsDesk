-- Business schema only. Database, roles, grants and storage are prepared separately, as part of the infrastructure exercises.
-- Apply once to an empty application schema; no IF NOT EXISTS hides a mismatched schema.
CREATE TABLE tickets (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  title varchar(120) NOT NULL CHECK (char_length(btrim(title)) >= 3),
  description varchar(2000) NOT NULL DEFAULT '',
  priority varchar(10) NOT NULL CHECK (priority IN ('low','normal','high')),
  status varchar(20) NOT NULL DEFAULT 'open' CHECK (status IN ('open','in_progress','closed')),
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);
