-- Enable fuzzy text search
create extension if not exists pg_trgm;

-- Custom function to run raw SQL (be careful!)
create or replace function run_sql(query text)
returns setof json as $$
begin
  return query execute query;
end;
$$ language plpgsql security definer;
