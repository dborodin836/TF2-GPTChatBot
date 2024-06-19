import React, { useEffect, useState } from 'react';
import Form from '@rjsf/mui';
import { RJSFSchema } from '@rjsf/utils';
import validator from '@rjsf/validator-ajv8';
import { useAlert } from '../AlertContext';


const log = (type: unknown) => console.log.bind(console, type);

export function CommandsPage() {
  const [schema, setSchema] = useState<RJSFSchema>({});
  const { openAlert } = useAlert();

  const fetchSchema = async () => {
    const response = await fetch('http://127.0.0.1:8000/schemas/command');
    if (!response.ok) {
      console.error('Failed to fetch command schema');
      openAlert('Failed to fetch command schema.');
    } else {
      const data = await response.json();
      setSchema(data);
    }
  };

  useEffect(() => {
    fetchSchema();
  }, []);

  return (
    <Form
      schema={schema}
      validator={validator}
      onChange={log('changed')}
      onSubmit={log('submitted')}
      onError={log('errors')}
    />
  );
}
