import { Textarea } from "@material-tailwind/react";

export function LogsArea() {
  return (
      <div className="flex flex-1 w-full flex-col gap-6 p-4">
          <Textarea className="min-w-[95%] min-h-[85vh]" size="lg" label="App logs"/>
      </div>
  );
}