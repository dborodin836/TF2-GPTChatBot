import React, { useEffect, useState } from 'react';
import Form from '@rjsf/mui';
import { RJSFSchema, UiSchema } from '@rjsf/utils';
import validator from '@rjsf/validator-ajv8';
import { useAlert } from '../AlertContext';


const log = (type: unknown) => console.log.bind(console, type);

const uiSchema: UiSchema = {
  'traits': {
    'items': {
      'ui:options': {
        'label': false,
      },
      '__id': {
        'ui:widget': 'hidden',
      },
    },
  },
};

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
      className="max-h-[calc(100vh-2rem)] text-gray-700 w-full gap-6 p-4 overflow-y-scroll"
      schema={schema}
      uiSchema={uiSchema}
      validator={validator}
      onChange={log('changed')}
      onSubmit={log('submitted')}
      onError={log('errors')}
    />
  );
}
