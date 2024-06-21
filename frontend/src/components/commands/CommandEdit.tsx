import React, { useEffect, useState } from 'react';
import Form from '@rjsf/mui';
import { RJSFSchema, UiSchema } from '@rjsf/utils';
import validator from '@rjsf/validator-ajv8';
import { useAlert } from '../AlertContext';
import { useNavigate, useParams } from 'react-router-dom';


const log = (type: unknown) => console.log.bind(console, type);

const uiSchema: UiSchema = {
  'ui:submitButtonOptions': {
    'submitText': 'Save',
    props: {
      className: '',
    },
  },
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

export function CommandEdit() {
  const [schema, setSchema] = useState<RJSFSchema>({});
  const [formData, setFormData] = useState<any>({});
  const { command } = useParams<{ command: string }>();
  const { openAlert } = useAlert();
  const navigate = useNavigate();

  const submitCommand = async ({ formData }: any) => {
    if (!formData) {
      console.log('No command to submit');
      return;
    }
    console.log(formData);

    const response = await fetch(`http://127.0.0.1:8000/command/edit/${command}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    });

    if (!response.ok) {
      const data = await response.json();
      console.log(data);
      openAlert(`Error occurred: ${JSON.stringify(data.err)}`);
    } else {
      navigate('/command/list')
      openAlert('Successfully edited command.');
    }
  };


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

  const fetchCommandMeta = async (command: string) => {
    const response = await fetch(`http://127.0.0.1:8000/command/meta/${command}`);
    if (!response.ok) {
      console.error('Failed to fetch command data');
      openAlert('Failed to fetch command data.');
    } else {
      const data = await response.json();
      setFormData(data);
    }
  };

  useEffect(() => {
    fetchSchema();
    if (command) {
      fetchCommandMeta(command);
    }
  }, []);

  return (
    <Form
      className="max-h-[calc(100vh-2rem)] text-gray-700 w-full gap-6 p-4 overflow-y-scroll"
      schema={schema}
      uiSchema={uiSchema}
      validator={validator}
      onChange={log('changed')}
      onSubmit={submitCommand}
      onError={log('errors')}
      formData={formData}
    />
  );
}
