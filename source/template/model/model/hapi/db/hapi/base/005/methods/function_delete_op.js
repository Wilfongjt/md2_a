'use strict';
// const pg = require('pg');

const Step = require('../../../../lib/runner/step');
module.exports = class CreateFunctionDeleteOP extends Step {
  constructor(baseName, baseVersion) {
    super(baseName, baseVersion);

    this.name = 'delete';
    this.name = `${this.kind}_${this.version}.${this.name}`;
    this.params = 'owner_id OWNERID, primary_key PRIMARYKEY';
    this.types = 'OWNERID, PRIMARYKEY';
    this.sql = `
    -- DROP FUNCTION if exists base_0_0_1.delete(OWNER, PRIMARYKEY);    

    DROP FUNCTION if exists ${this.name}(${this.types});    

    CREATE OR REPLACE FUNCTION ${this.name}(${this.params}) RETURNS JSONB

    AS $$

      declare _count integer := -1;
      
      BEGIN
 
        -- [Function: Delete by PrimaryKey]
        -- [Description: Delete object by primary_key (pk,sk)]
        
        -- [Validate owner_id]

          if owner_id is NULL then
            -- [Fail 400 when a owner_id parameter is NULL]
            return '{"method":"delete", "status":"400","msg":"Bad Request"}'::JSONB;
          end if;      

          if owner_id.id is NULL then
              return '{"method":"delete", "status":"400","msg":"Bad Request", "extra":"owner_id.id is NULL"}'::JSONB;
          end if;

          -- [Validate primary_key]

          if primary_key is NULL then
            -- [Fail 400 when a primary_key parameter is NULL]
              return '{"method":"delete", "status":"400","msg":"Bad Request", "extra":"primary_key is NULL"}'::JSONB;
          end if;

          if primary_key.pk is NULL then
            -- [Fail 400 when a primary_key.pk parameter is NULL]
              return '{"method":"delete", "status":"400","msg":"Bad Request", "extra":"primary_key.pk is NULL"}'::JSONB;
          end if;

          if primary_key.sk is NULL then
            -- [Fail 400 when a primry_key.sk parameter is NULL]
              return '{"method":"delete", "status":"400","msg":"Bad Request", "extra":"primary_key.sk is NULL"}'::JSONB;
          end if;

          -- [Match Owner]
                    
          if not exists(select t.pk 
                 from base_0_0_1.one t 
                 where t.pk=primary_key.pk 
                       and t.sk='name#owner'
                       and t.tk=format('value#%s', owner_id.id)) then
              return format('{"method":"delete", "status":"404", "msg":"Not Found", "extra":"E bad key", "key":"%s", "pk":"%s", "sk":"%s"}',owner_id.id, primary_key.pk, primary_key.sk)::JSONB;
          end if;
          
          BEGIN
              -- what about sk=name#owner records?
              -- strategies: 1) encode pk or sk with owner id
              --             2) exists(select where pk=primary_key.pk and tk=owner_id.id)
                          
                  if strpos(primary_key.sk,'*') > 0 then
        
                      -- [Delete all items in a group]
                      WITH deleted AS (Delete from ${this.kind}_${this.version}.one t
                                        where t.pk=primary_key.pk
                                        RETURNING *) SELECT count(*) into _count FROM deleted;
                  else

                      -- [Delete specific item]
                      -- [Dont delete owner triple]
                      WITH deleted AS (Delete from base_0_0_1.one t
                                        where t.pk=primary_key.pk::TEXT
                                        and t.sk=primary_key.sk::TEXT
                                        and t.sk <> format('name#owner',owner_id.id) 
                                        RETURNING *) SELECT count(*) into _count FROM deleted;
                  end if;
              
          EXCEPTION
              when others then
                RAISE NOTICE '5A Beyond here there be dragons! %', sqlstate;
                return format('{"method":"delete", "status":"%s", "msg":"Internal Server Error", "owner_id":"%s", "primary_key":"%s"}', sqlstate, owner_id, primary_key)::JSONB ;
          END;

          -- [Return {status,msg,criteria,deletion}]

          return format('{"method":"delete","status":"200", "msg":"OK", "owner_id": "%s", "primary_key": "%s", "deletion":{"count":%s}}',owner_id::TEXT, primary_key::TEXT, _count)::JSONB ;

      END;

      $$ LANGUAGE plpgsql;

    -- GRANT: Grant Execute

    /* Doesnt work in Hobby
        
    grant EXECUTE on FUNCTION ${this.name}(TRIPLE,OWNERID) to api_user;
    */
    `;
    // console.log('-- [Create Delete Function]\n', this.sql);
  }    
};

