'use strict';
// const pg = require('pg');
// PrimaryKey
// pk=key.pk and sk=key.sk ---> delete one
// pk=key.pk and sk='*'    ---> delete all like key.pk
// SecondaryKey
// sk=key.sk and tk=key.tk ---> delete one
//

const Step = require('../../../lib/runner/step');
module.exports = class CreateFunctionDelete001 extends Step {
  constructor(baseName, baseVersion) {
    super(baseName, baseVersion);
    // this.kind = kind;
    this.name = 'delete';
    this.name = `${this.kind}_${this.version}.${this.name}`;
    // this.params = 'criteria JSONB, owner_key OWNER_ID, ';
    this.params = 'criteria JSONB, owner_key OWNER_ID';
    this.sql = `
    CREATE OR REPLACE FUNCTION ${this.name}(${this.params}) RETURNS JSONB

    AS $$

      declare _result record;
      declare _status TEXT;
      declare _msg TEXT;
      declare _rc JSONB;
      declare _count integer;

      BEGIN
        -- [Function: Delete by Primary Criteria {pk,sk} or {sk,tk}]
        -- [Description: Delete User by primary key {pk,sk}]

        -- [Validate Criteria]

          criteria := ${this.kind}_${this.version}.validate_criteria(criteria);
          if criteria is NULL then
            -- [Fail 400 when a criteria parameter is NULL]
            return format('{"status":"400","msg":"Bad Request","step":"%s"}',_step)::JSONB;
          end if;

          BEGIN

              --_crit := criteria::JSONB;
              -- there can be only one
              -- strpos(criteria ->> 'sk', '*') > 0
              -- if criteria ? 'pk' and criteria ? 'sk' and criteria ->> 'sk' = '*' then
              if criteria ? 'pk' and criteria ? 'sk' and strpos(criteria ->> 'sk', '*') > 0 then
              
                  -- [Delete where pk and sk]

                  -- cant return more than one rec, so return a
                  -- Delete from ${this.kind}_${this.version}.one
                  --  where lower(pk)=lower(criteria ->> 'pk')
                  --       and owner=owner_key.id;
                          
                  WITH deleted AS (Delete from ${this.kind}_${this.version}.one
                                    where lower(pk)=lower(criteria ->> 'pk')
                                    and owner=owner_key.id RETURNING *) SELECT count(*) into _count FROM deleted;
   

                   return format('{"status":"200", "msg":"OK", "criteria":%s, "deletion":{"count":"%s"}}',criteria, _count)::JSONB ;

              elsif criteria ? 'pk' and criteria ? 'sk' then
                -- [Delete where pk and sk]

                  Delete from ${this.kind}_${this.version}.one
                    where lower(pk)=lower(criteria ->> 'pk')
                          and sk=criteria ->> 'sk'
                          and owner=owner_key.id
                    returning * into _result;

              elsif criteria ? 'sk' and criteria ? 'tk' then
                Delete from ${this.kind}_${this.version}.one
                  where sk=criteria ->> 'sk' and tk=criteria ->> 'tk'
                  and owner=owner_key.id
                  returning * into _result;
              else
                  return format('{"status":"400", "msg":"Bad Request", "criteria":%s}',criteria)::JSONB ;
              end if;

              -- [Remove password from results when found]
              _rc :=  to_jsonb(_result)  #- '{form,password}';
              if _rc ->> 'pk' is NULL then
                -- [Fail 404 when primary key is not found]
                -- [Fail 404 when item is not owned by current]
                return format('{"status":"404", "msg":"Not Found", "owner":"%s", "criteria":%s}', owner_key.id, criteria)::JSONB ;
              end if;
          EXCEPTION
              when others then
                RAISE NOTICE '5 Beyond here there be dragons! %', sqlstate;
                return format('{"status":"%s", "msg":"Internal Server Error", "criteria":%s}',sqlstate,criteria)::JSONB ;
          END;

          -- [Return {status,msg,criteria,deletion}]
          return format('{"status":"200", "msg":"OK", "criteria":%s, "deletion":%s}',criteria,_rc::TEXT)::JSONB ;

      END;

      $$ LANGUAGE plpgsql;

    -- GRANT: Grant Execute

    /* Doesnt work in Hobby
    grant EXECUTE on FUNCTION ${this.name}(JSONB,TEXT) to api_user;
    */
    `;
    // console.log(this.sql);
    }
    getName() {
      return `${this.name}(${this.params})`;
    }
};
