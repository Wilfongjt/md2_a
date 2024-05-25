'use strict';
// [query by MBR]
// [query by pk, sk]
// [query by pk, sk, owner]

const Step = require('../../../lib/runner/step');
module.exports = class FunctionQuery extends Step {
  constructor(baseName, baseVersion) {
    super(baseName, baseVersion);
    // this.kind = kind;
    this.version = `${baseName}_${baseVersion}`;
    
    this.name = 'get';
    this.name = `${this.version}.${this.name}`;
    this.params = 'm_b_r MBR';
    this.types = 'MBR';
    this.return = 'JSONB';
    this.sql = `
        DROP FUNCTION if exists ${this.name}(${this.types});    
    /*
    CREATE OR REPLACE FUNCTION ${this.name}(${this.params}) RETURNS ${this.return}

    AS $$
      declare _result JSONB;
      DECLARE mbr BOOLEAN;
    BEGIN
      -- [Function: Query by MBR ]
      -- [Description: MBR search]
    
      BEGIN

        -- if mbr then
        select pk, sk, tk from base_0_0_1.one 
         where pk in (select pk from base_0_0_1.one 
             where sk ='coordinate' and (tk::COORDINATE).lat >= m_b_r.south 
                                    and (tk::COORDINATE).lat <= m_b_r.north
                                    and (tk::COORDINATE).lon >= m_b_r.west
                                    and (tk::COORDINATE).lon <= m_b_r.east);
          
        -- else
    
        --  -- [Fail 400 when unexpecte Search Pattern]
        --  return format('{"status:"400","msg":"Bad Request", "extra":"B%s"}', sqlstate)::JSONB;
    
        -- end if;
    
      EXCEPTION
    
          when others then
            
            return format('{"status":"400","msg":"Bad Request", "extra":"C %s"}',sqlstate)::JSONB;
    
      END;
        
      if _result is NULL then    
        -- [Fail 200 when query results are empty ]

        return '{"status":"404", "msg":"Not Found", "selection": []}'::JSONB;
    
      end if;
    
      -- [Return {status,msg,selection}]
      return format('{"status":"200", "msg":"OK", "selection": %s}', _result)::JSONB;
    
    END;
            
    $$ LANGUAGE plpgsql;
        */
         
    
    /* Doesnt work in Hobby
    --grant EXECUTE on FUNCTION ${this.name}(JSONB, TEXT) to api_guest;
    
    grant EXECUTE on FUNCTION ${this.name}(JSONB, TEXT) to api_user;
    
    grant EXECUTE on FUNCTION ${this.name}(JSONB, TEXT) to api_admin;
    */
    `;
    // console.log('CreateFunction', this.sql);
  }    
  getName() {
    return `${this.name}(${this.params}) ${this.return}`;
  }
};