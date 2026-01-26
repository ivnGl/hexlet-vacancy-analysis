declare module '*.jsx.svg' {
  import { FunctionComponent, SVGProps } from 'react';

  const svg: FunctionComponent<SVGProps<SVGSVGElement> & { title?: string }>;
  export default svg;
}

declare module '*.svg' {
  const src: string;
  export default src;
}