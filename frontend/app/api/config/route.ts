import { NextResponse } from 'next/server';
import { getConfig } from '../../../utils/env-config';

export async function GET() {
  try {
    const config = getConfig();
    
    // Only return public configuration that's safe to expose to the client
    const publicConfig = {
      app: config.app,
      ui: config.ui,
      features: config.features,
      upload: config.upload,
    };

    return NextResponse.json({
      success: true,
      config: publicConfig,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    console.error('Config API error:', error);
    return NextResponse.json(
      {
        success: false,
        error: 'Failed to load configuration',
        timestamp: new Date().toISOString(),
      },
      { status: 500 }
    );
  }
}