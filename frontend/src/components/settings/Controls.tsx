import { Card } from '@material-tailwind/react';
import { ArrowPathIcon, CheckIcon, XMarkIcon } from '@heroicons/react/16/solid';
import React from 'react';
import * as PropTypes from 'prop-types';

export function Controls(props: {
  submit: React.MouseEventHandler<HTMLDivElement> | undefined;
  discard: React.MouseEventHandler<HTMLDivElement> | undefined;
  getDefaults: React.MouseEventHandler<HTMLDivElement> | undefined;
}) {
  return (
    <Card className="flex border rounded-none shadow-none flex-row p-4 gap-6">
      <div
        role="button"
        onClick={props.submit}
        className="flex items-center w-51 hover:border-green-500 border-2 p-3 rounded-lg text-start leading-tight transition-all hover:bg-teal-50 hover:bg-opacity-80 active:bg-teal-50 active:bg-opacity-80 hover:text-green-700 active:text-green-700 outline-none"
      >
        <div className="grid place-items-center mr-4">
          <CheckIcon className="h-5 w-5" />
        </div>
        Save Changes
      </div>

      <div
        role="button"
        onClick={props.discard}
        className="flex items-center w-51 hover:border-red-500 border-2 p-3 rounded-lg text-start leading-tight transition-all hover:bg-red-50 hover:bg-opacity-80 active:bg-red-50 active:bg-opacity-80 hover:text-red-900 active:text-red-900 outline-none"
      >
        <div className="grid place-items-center mr-4">
          <XMarkIcon className="h-5 w-5" />
        </div>
        Discard Changes
      </div>

      <div
        role="button"
        onClick={props.getDefaults}
        className="flex items-center w-51 hover:border-blue-500 border-2 p-3 rounded-lg text-start leading-tight transition-all hover:bg-blue-50 hover:bg-opacity-80 active:bg-blue-50 active:bg-opacity-80 hover:text-light-blue-900 active:text-light-blue-900 outline-none"
      >
        <div className="grid place-items-center mr-4">
          <ArrowPathIcon className="h-5 w-5" />
        </div>
        Restore Defaults
      </div>
    </Card>
  );
}

Controls.propTypes = {
  onClick: PropTypes.func,
  onClick1: PropTypes.func,
  onClick2: PropTypes.func,
};
