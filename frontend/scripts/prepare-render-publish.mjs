import { cpSync, existsSync, mkdirSync, rmSync } from "node:fs";
import { resolve } from "node:path";

const workspaceRoot = resolve(process.cwd());
const outDir = resolve(workspaceRoot, "frontend", "out");
const renderPublishDir = resolve(workspaceRoot, "npm start");

if (!existsSync(outDir)) {
  throw new Error(`Expected static export directory not found: ${outDir}`);
}

rmSync(renderPublishDir, { recursive: true, force: true });
mkdirSync(renderPublishDir, { recursive: true });
cpSync(outDir, renderPublishDir, { recursive: true });

console.log(`Prepared Render publish directory at: ${renderPublishDir}`);
