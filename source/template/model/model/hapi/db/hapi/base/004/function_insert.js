'use strict';
// const pg = require('pg');

const Step = require('../../../lib/runner/step');
module.exports = class CreateFunctionInsert001 extends Step {
  constructor(baseName, baseVersion) {
    super(baseName, baseVersion);
    // this.kind = kind;
    this.name = 'insert';
    this.name = `${this.kind}_${this.version}.${this.name}`;
    this.sql = `CREATE OR REPLACE FUNCTION ${this.name}(_chelate JSONB, owner OWNER_ID) RETURNS JSONB

    AS $$
        
      declare _form JSONB;
    
      declare _result record;
    
      declare _extra TEXT;
    
    BEGIN
    
      -- [Function: Insert Chelate like {pk,sk,tk,form}, {pk,sk,form}, {sk,tk,form}, or {sk,form}]
    
      -- [Validate Chelate]
    
      if _chelate is NULL then
    
        -- [Fail 400 when a parameter is NULL]
    
        return '{"status":"400","msg":"Bad Request", "extra":"chelate is NULL"}'::JSONB;
    
      end if;
    
      BEGIN
    
          _form := (_chelate ->> 'form')::JSONB;
    
    
          if owner.id = '0' then
    
            -- [Insert requires an owner owner.id value]
    
            return '{"status":"400", "msg":"Bad Request", "extra":"chelate is missing owner."}'::JSONB;
    
          end if;
    
          if not(_chelate ? 'form') then -- MISSING FORM
    
            -- [Fail 400 when chelate is missig a form]
    
            return '{"status":"400", "msg":"Bad Request", "extra":"chelate is missing form."}'::JSONB;
    
          end if;
    
          -- pksktk
    
          -- [Insert Unique Chelate]
    
          if _chelate ? 'pk' and _chelate ? 'sk' and _chelate ? 'tk' then
    
            -- [Handle chelate with pk, sk and tk]
    
            _extra := 'A';
    
            insert into ${this.kind}_${this.version}.one (pk,sk,tk,form,owner)
    
              values (lower(_chelate ->> 'pk'), (_chelate ->> 'sk'), (_chelate ->> 'tk'), _form, owner.id)
    
              returning * into _result;
    
            --raise notice 'A insert form %',_form;
    
          -- pksk
    
          elsif _chelate ? 'pk' and _chelate ? 'sk' then
    
            -- [Handle chelate with pk and sk]
    
            _extra := 'B';
    
            insert into ${this.kind}_${this.version}.one (pk,sk,form,owner)
    
              values (lower(_chelate ->> 'pk'), (_chelate ->> 'sk') ,_form, owner.id)
    
              returning * into _result;
    
            --raise notice 'B insert form %',_form;
    
          -- sktk
    
          elsif _chelate ? 'sk' and _chelate ? 'tk' then
    
            -- [Handle chelate with sk and tk]
    
            _extra := 'C';
    
            insert into ${this.kind}_${this.version}.one (sk,tk,form,owner)
              values ((_chelate ->> 'sk'), (_chelate ->> 'tk') ,_form, owner.id)
              returning * into _result;
    
            --raise notice 'C insert form %',_form;
  
          -- sk
    
          elsif _chelate ? 'sk' then
    
            -- [Handle chelate with sk]
    
            _extra := 'D';
    
            insert into ${this.kind}_${this.version}.one (sk,form,owner)
              values (
                      (_chelate ->> 'sk'),
                      _form, owner.id) returning * into _result;
    
            --raise notice 'D insert form %',_form;
    
          else
    
            -- [Fail 400 when chelate is missing a proper set of keys (pk,sk,tk),(pk,sk),(sk,tk), or (sk)]
    
            return '{"status":"400", "msg":"Bad Request", "extra":"failed insert"}'::JSONB;
    
          end if;
    
              --raise notice 'insert 3';
    
        EXCEPTION
    
             -- when sqlstate 'PT400' then
    
             --   return '{"status":"400", "msg":"Bad Request"}'::JSONB;
    
              when unique_violation then
    
                -- [Fail 409 when duplicate]
    
                return '{"status":"409", "msg":"Duplicate"}'::JSONB;
    
              when others then
    
                RAISE NOTICE 'Insert Beyond here there be dragons! %', sqlstate;
    
                return format('{"status":"%s", "msg":"Unhandled","extra":"%s","owner":"%s","chelate":%s}', sqlstate, _extra,owner.id,_chelate)::JSONB;
    
        END;
    
        -- [Return {status,msg,insertion}]
        
        return format('{"status":"200", "msg":"OK", "insertion": %s}',(to_jsonb(_result)#- '{form,password}')::TEXT)::JSONB;    
    
    
    END;
    
    $$ LANGUAGE plpgsql;
    
    /* Doesnt work in Hobby
    
    --grant EXECUTE on FUNCTION ${this.name}.insert(JSONB) to api_guest;
    
    grant EXECUTE on FUNCTION ${this.name}.insert(JSONB,TEXT) to api_user;
    */
    `;
    // console.log('CreateFunction', this.sql);
  }    
};