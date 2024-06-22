import React from 'react';
import { LineChart } from '@mui/x-charts/LineChart';
import { Typography } from '@material-tailwind/react';

const years = [
  new Date(1990, 0, 1),
  new Date(1991, 0, 1),
  new Date(1992, 0, 1),
  new Date(1993, 0, 1),
  new Date(1994, 0, 1),
  new Date(1995, 0, 1),
  new Date(1996, 0, 1),
  new Date(1997, 0, 1),
  new Date(1998, 0, 1),
  new Date(1999, 0, 1),
  new Date(2000, 0, 1),
  new Date(2001, 0, 1),
  new Date(2002, 0, 1),
  new Date(2003, 0, 1),
  new Date(2004, 0, 1),
  new Date(2005, 0, 1),
  new Date(2006, 0, 1),
  new Date(2007, 0, 1),
  new Date(2008, 0, 1),
  new Date(2009, 0, 1),
  new Date(2010, 0, 1),
  new Date(2011, 0, 1),
  new Date(2012, 0, 1),
  new Date(2013, 0, 1),
  new Date(2014, 0, 1),
  new Date(2015, 0, 1),
  new Date(2016, 0, 1),
  new Date(2017, 0, 1),
  new Date(2018, 0, 1),
];

const FranceGDPperCapita = [
  28129, 28294.264, 28619.805, 28336.16, 28907.977, 29418.863, 29736.645, 30341.807,
  31323.078, 32284.611, 33409.68, 33920.098, 34152.773, 34292.03, 35093.824,
  35495.465, 36166.16, 36845.684, 36761.793, 35534.926, 36086.727, 36691, 36571,
  36632, 36527, 36827, 37124, 37895, 38515.918,
];

const UKGDPperCapita = [
  26189, 25792.014, 25790.186, 26349.342, 27277.543, 27861.215, 28472.248, 29259.764,
  30077.385, 30932.537, 31946.037, 32660.441, 33271.3, 34232.426, 34865.78,
  35623.625, 36214.07, 36816.676, 36264.79, 34402.36, 34754.473, 34971, 35185, 35618,
  36436, 36941, 37334, 37782.83, 38058.086,
];

const GermanyGDPperCapita = [
  25391, 26769.96, 27385.055, 27250.701, 28140.057, 28868.945, 29349.982, 30186.945,
  31129.584, 32087.604, 33367.285, 34260.29, 34590.93, 34716.44, 35528.715,
  36205.574, 38014.137, 39752.207, 40715.434, 38962.938, 41109.582, 43189, 43320,
  43413, 43922, 44293, 44689, 45619.785, 46177.617,
];

const categories: { [key: string]: string[] } = {
  Category10: [
    '#1f77b4',
    '#ff7f0e',
    '#2ca02c',
    '#d62728',
    '#9467bd',
    '#8c564b',
    '#e377c2',
    '#7f7f7f',
    '#bcbd22',
    '#17becf',
  ],
  Accent: [
    '#7fc97f',
    '#beaed4',
    '#fdc086',
    '#ffff99',
    '#386cb0',
    '#f0027f',
    '#bf5b17',
    '#666666',
  ],
  Dark2: [
    '#1b9e77',
    '#d95f02',
    '#7570b3',
    '#e7298a',
    '#66a61e',
    '#e6ab02',
    '#a6761d',
    '#666666',
  ],
  Paired: [
    '#a6cee3',
    '#1f78b4',
    '#b2df8a',
    '#33a02c',
    '#fb9a99',
    '#e31a1c',
    '#fdbf6f',
    '#ff7f00',
    '#cab2d6',
    '#6a3d9a',
    '#ffff99',
    '#b15928',
  ],
  Pastel1: [
    '#fbb4ae',
    '#b3cde3',
    '#ccebc5',
    '#decbe4',
    '#fed9a6',
    '#ffffcc',
    '#e5d8bd',
    '#fddaec',
    '#f2f2f2',
  ],
  Pastel2: [
    '#b3e2cd',
    '#fdcdac',
    '#cbd5e8',
    '#f4cae4',
    '#e6f5c9',
    '#fff2ae',
    '#f1e2cc',
    '#cccccc',
  ],
  Set1: [
    '#e41a1c',
    '#377eb8',
    '#4daf4a',
    '#984ea3',
    '#ff7f00',
    '#ffff33',
    '#a65628',
    '#f781bf',
    '#999999',
  ],
  Set2: [
    '#66c2a5',
    '#fc8d62',
    '#8da0cb',
    '#e78ac3',
    '#a6d854',
    '#ffd92f',
    '#e5c494',
    '#b3b3b3',
  ],
  Set3: [
    '#8dd3c7',
    '#ffffb3',
    '#bebada',
    '#fb8072',
    '#80b1d3',
    '#fdb462',
    '#b3de69',
    '#fccde5',
    '#d9d9d9',
    '#bc80bd',
    '#ccebc5',
    '#ffed6f',
  ],
  Tableau10: [
    '#4e79a7',
    '#f28e2c',
    '#e15759',
    '#76b7b2',
    '#59a14f',
    '#edc949',
    '#af7aa1',
    '#ff9da7',
    '#9c755f',
    '#bab0ab',
  ],
};

export function Dashboard() {
  const [colorScheme, setColorScheme] = React.useState('Accent');

  return (
    <>
      <div className="w-[100%] h-[50%] text-gray-700 p-4">
        <Typography variant="h3" className="mt-4 ms-3">
          Command usage
        </Typography>
        <LineChart
          xAxis={[
            {
              id: 'Years',
              data: years,
              scaleType: 'time',
              valueFormatter: (date) => date.getFullYear().toString(),
            },
          ]}
          series={[
            {
              id: 'France',
              data: FranceGDPperCapita,
              stack: 'total',
              area: true,
              curve: 'natural',
              showMark: false,
            },
            {
              id: 'Germany',
              data: GermanyGDPperCapita,
              stack: 'total',
              area: true,
              curve: 'natural',
              showMark: false,
            },
            {
              id: 'United Kingdom',
              data: UKGDPperCapita,
              stack: 'total',
              area: true,
              curve: 'natural',
              showMark: false,
            },
          ]}
          colors={categories[colorScheme]}
          margin={{ right: 20, left: 70, top: 20 }} />
      </div>
      <div className="w-[100%] h-[50%] text-gray-700 p-4">
        <Typography variant="h3" className="mt-4 ms-3">
          Command usage
        </Typography>
        <LineChart
          xAxis={[
            {
              id: 'Years',
              data: years,
              scaleType: 'time',
              valueFormatter: (date) => date.getFullYear().toString(),
            },
          ]}
          series={[
            {
              id: 'France',
              data: FranceGDPperCapita,
              stack: 'total',
              area: true,
              curve: 'natural',
              showMark: false,
            },
            {
              id: 'Germany',
              data: GermanyGDPperCapita,
              stack: 'total',
              area: true,
              curve: 'natural',
              showMark: false,
            },
            {
              id: 'United Kingdom',
              data: UKGDPperCapita,
              stack: 'total',
              area: true,
              curve: 'natural',
              showMark: false,
            },
          ]}
          colors={categories[colorScheme]}
          margin={{ right: 20, left: 70, top: 20 }} />
      </div>
    </>
  )
    ;
}
