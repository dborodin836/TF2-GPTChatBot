import { Card, Input, Typography } from '@material-tailwind/react';
import { ExclamationTriangleIcon } from '@heroicons/react/24/solid';
import * as PropTypes from 'prop-types';
import React from 'react';
import { Settings } from './SettingsType';

export function RequireSettings(props: {
  settings: Settings | null;
  onChangeInput: React.ChangeEventHandler<HTMLInputElement> | undefined;
}) {
  return (
    <Card className="p-6 mt-15 w-full">
      <Typography className="mb-3" variant="h2">
        <span className="flex items-center">
          Required Settings{' '}
          <ExclamationTriangleIcon className="h-8 w-8 text-red-500 ml-2 inline-block align-middle" />
        </span>
      </Typography>
      <hr className="mb-3" />
      <div className="mb-3">
        <label className="mb-2 inline-block text-neutral-500 dark:text-neutral-400">
          console.log file location
        </label>
        <div className="min-w-[100%]">
          <Input
            className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
            labelProps={{
              className: 'hidden',
            }}
            containerProps={{ className: 'min-w-[100px]' }}
            value={props.settings ? props.settings.TF2_LOGFILE_PATH : ''}
            name="TF2_LOGFILE_PATH"
            onChange={props.onChangeInput}
          />
        </div>
      </div>
    </Card>
  );
}

RequireSettings.propTypes = {
  settings: PropTypes.any,
  onChangeInput: PropTypes.func,
};
