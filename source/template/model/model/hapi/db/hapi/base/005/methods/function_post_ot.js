'use strict';
// const pg = require('pg');
// post a {pk:<group-type>#<group-value>, sk, tk}
const Step = require('../../../lib/runner/step');
module.exports = class CreateFunctionPostOT extends Step {
  constructor(baseName, baseVersion) {
    super(baseName, baseVersion);

    this.name = 'post';
    this.name = `${this.kind}_${this.version}.${this.name}`;
    this.params = 'owner OWNERID, trip TRIPLE';
    this.types = 'OWNERID, TRIPLE';

    this.sql = `
DROP FUNCTION if exists ${this.name}(${this.types});    

CREATE OR REPLACE FUNCTION ${this.name}(${this.params}) RETURNS JSONB

    AS $$
      declare _result record;
      declare _extra TEXT;
    
    BEGIN
        -- [Validate OwnerId]
        
        if owner is NULL then
            -- [Fail 400 when a owner parameter is NULL]
            return '{"status":"400","msg":"Bad Request", "extra":"owner is NULL"}'::JSONB;
        end if;
            
        if owner.id is NULL then
          -- [Fail 400 when owner.id a parameter is NULL]
          return '{"status":"400","msg":"Bad Request", "extra":"owner.id is NULL"}'::JSONB;
        end if;  
        
      -- [Function: Insert triple like (pk,sk,tk)]
    
      -- [Validate Triple]
    
      if trip is NULL then
    
        -- [Fail 400 when a parameter is NULL]
    
        return '{"status":"400","msg":"Bad Request", "extra":"triple is NULL"}'::JSONB;
    
      end if;
            
      if trip.pk is NULL then
    
        -- [Fail 400 when triple.pk a parameter is NULL]
    
        return '{"status":"400","msg":"Bad Request", "extra":"triple.pk is NULL"}'::JSONB;
    
      end if;      
      
      if trip.sk is NULL then
    
        -- [Fail 400 when triple.sk parameter is NULL]
    
        return '{"status":"400","msg":"Bad Request", "extra":"triple.sk is NULL"}'::JSONB;
    
      end if;
      
      if trip.tk is NULL then
    
        -- [Fail 400 when triple.tk parameter is NULL]
    
        return '{"status":"400","msg":"Bad Request", "extra":"triple is NULL"}'::JSONB;
    
      end if;
      
      if strpos(trip.pk,'#') = 0 then
         return '{"status":"400","msg":"Bad Request", "extra":"malformed triple.pk"}'::JSONB;
      end if;
      
      if strpos(trip.sk,'#') = 0 then
         return '{"status":"400","msg":"Bad Request", "extra":"malformed triple.sk"}'::JSONB;
      end if;
      
      if strpos(trip.tk,'#') = 0 then
         return '{"status":"400","msg":"Bad Request", "extra":"malformed triple.tk"}'::JSONB;
      end if;   
         
      BEGIN
    
          -- [Insert Unique Triple]
    
          insert into base_0_0_1.one (pk,sk,tk,form,owner)
            values (trip.pk, trip.sk, trip.tk, '{"id":"DEPRECATED"}'::JSONB, owner.id)
            returning * into _result;
        
        EXCEPTION
    
              when unique_violation then
    
                -- [Fail 409 when duplicate]
    
                return format('{"status":"409", "msg":"Duplicate", "triple": "%s"}', trip::TEXT)::JSONB;
    
              when others then
    
                RAISE NOTICE 'Insert Beyond here there be dragons! %', sqlstate;
    
                return format('{"status":"%s", "msg":"Unhandled","extra":"%s","owner":"%s","triple":"%s"}', sqlstate, _extra,owner.id,trip::TEXT)::JSONB;
    
        END;
    
        -- [Return {status,msg,insertion}]
        
        return format('{"status":"200", "msg":"OK", "insertion": %s}',(to_jsonb(_result)#- '{form,password}')::TEXT)::JSONB;    
    
    
    END;
    
    $$ LANGUAGE plpgsql;
    
    /* Doesnt work in Hobby
        
    grant EXECUTE on FUNCTION ${this.name}(TRIPLE,OWNERID) to api_user;
    */
    `;
    // console.log('-- Create Post Function\n', this.sql);
  }    
};

