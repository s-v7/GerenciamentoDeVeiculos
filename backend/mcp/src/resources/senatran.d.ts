import { ResourceTemplate } from "@modelcontextprotocol/server";
export declare const senatranUfResource: ResourceTemplate;
export declare function readSenatranUf(uri: URL, variables: Record<string, string | string[]>): Promise<{
    contents: {
        uri: string;
        mimeType: string;
        text: string;
    }[];
}>;
//# sourceMappingURL=senatran.d.ts.map