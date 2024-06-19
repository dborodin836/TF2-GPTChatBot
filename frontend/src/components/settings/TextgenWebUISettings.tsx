import { Card, Input, Typography } from '@material-tailwind/react';
import React from 'react';
import * as PropTypes from 'prop-types';
import { Settings } from './SettingsType';

export function TextgenWebUISettings(props: {
  settings: Settings | null;
  onChangeToggle: any;
  onChangeInput: any;
}) {
  return (
    <Card className="p-6 w-full">
      <Typography className="mb-3" variant="h2">
        Text Generation WebUI
      </Typography>
      <hr className="mb-3" />

      <div className="mb-3">
        <label className="mb-2 inline-block text-neutral-500 dark:text-neutral-400">
          Custom Model Host
        </label>
        <div className="min-w-[100%]">
          <Input
            className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
            labelProps={{
              className: 'hidden',
            }}
            containerProps={{ className: 'min-w-[100px]' }}
            value={props.settings ? props.settings.CUSTOM_MODEL_HOST : ''}
            name="CUSTOM_MODEL_HOST"
            onChange={props.onChangeInput}
          />
        </div>
      </div>
    </Card>
  );
}

TextgenWebUISettings.propTypes = {
  settings: PropTypes.any,
  onChangeToggle: PropTypes.func,
  onChangeInput: PropTypes.func,
};
