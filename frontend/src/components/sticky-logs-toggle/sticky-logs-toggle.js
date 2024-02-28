import { Switch, Typography } from "@material-tailwind/react";

export function StickyLogsToggle() {
  return (
    <Switch
      label={
        <div>
          <Typography color="blue-gray" className="font-medium">
            Sticky logs
          </Typography>
          <Typography variant="small" color="gray" className="font-normal">
            WIP: Auto scrolls to the latest logs. Disable if you need to copy something.
          </Typography>
        </div>
      }
      containerProps={{
        className: "-mt-15",
      }}
    />
  );
}