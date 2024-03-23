import React from "react";
import {Typography} from "@material-tailwind/react";

export function About() {
    return (
        <div className="flex flex-1 flex-col text-gray-700 w-full h-screen items-center justify-center gap-6 p-4">
            <img
                className="max-w-[15vw] rounded-full object-cover object-center"
                src="https://camo.githubusercontent.com/3b6b91909e8d5d8b03f8d52a2eb55041a9b0cb2b49ac430b77822a4fb10c610d/68747470733a2f2f692e706f7374696d672e63632f447776795a7171762f696d676f6e6c696e652d636f6d2d75612d5265706c6163652d436f6c6f722d45333832322d52766136372d44623573322e6a7067"
            />
            <Typography variant="h1">TF2-GPTChatBot</Typography>
            <Typography variant="h5">Source code is available on <a className="font-medium text-green-500 dark:text-green-blue-600 hover:underline" target="_blank" rel="noreferrer" href="https://github.com/dborodin836/TF2-GPTChatBot">GitHub</a></Typography>
            <Typography className="mt-0" variant="h4">Thank you for your interest! ❤️</Typography>
        </div>
    );
}