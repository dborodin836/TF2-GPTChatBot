import {Card, Radio, Typography} from "@material-tailwind/react";
import React from "react";
import * as PropTypes from "prop-types";

export function RTDSettings(props) {
    return <Card className="p-6 w-full">
        <Typography className="mb-3" variant="h2">RTD (Roll The Dice)</Typography>

        <hr className="mb-3"/>

        <label className="mb-2 inline-block text-neutral-500 dark:text-neutral-400">
            RTD Mode
        </label>
        <div className="w-[100%]">
            <div className="flex gap-8">
                <Radio
                    name="description"
                    label={
                        <div>
                            <Typography color="blue-gray" className="font-medium">
                                Disabled
                            </Typography>
                            <Typography variant="small" color="gray" className="font-normal">
                                Disable module functionality.
                            </Typography>
                        </div>
                    }
                    checked={props.settings?.RTD_MODE === 0 || false}
                    onChange={props.onChangeRadio0}
                    containerProps={{
                        className: "-mt-5",
                    }}
                />
                <Radio
                    name="description"
                    label={
                        <div>
                            <Typography color="blue-gray" className="font-medium">
                                RickRoll
                            </Typography>
                            <Typography variant="small" color="gray" className="font-normal">
                                Sends the RickRoll link (<a target="_blank" rel="noreferrer"
                                                            className="font-medium text-green-500 dark:text-green-blue-600 hover:underline"
                                                            href="https://youtu.be/dQw4w9WgXcQ">youtu.be/dQw4w9WgXcQ</a>).
                            </Typography>
                        </div>
                    }
                    checked={props.settings?.RTD_MODE === 1 || false}
                    onChange={props.onChangeRadio1}
                    containerProps={{
                        className: "-mt-5",
                    }}
                />
                <Radio
                    name="description"
                    label={
                        <div>
                            <Typography color="blue-gray" className="font-medium">
                                Random YouTube Meme
                            </Typography>
                            <Typography variant="small" color="gray" className="font-normal">
                                Sends a random link from vids.txt file.
                            </Typography>
                        </div>
                    }
                    checked={props.settings?.RTD_MODE === 2 || false}
                    onChange={props.onChangeRadio2}
                    containerProps={{
                        className: "-mt-5",
                    }}
                />
            </div>
        </div>
    </Card>;
}

RTDSettings.propTypes = {
    settings: PropTypes.any,
    onChangeRadio0: PropTypes.func,
    onChangeRadio1: PropTypes.func,
    onChangeRadio2: PropTypes.func
};