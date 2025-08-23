/**
 * ML-Powered Financial Analysis Service
 * Node.js wrapper for the Python ML Financial Analysis Engine
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs').promises;
const { v4: uuidv4 } = require('uuid');

class MLFinancialAnalysisService {
  constructor() {
    this.pythonPath = path.join(__dirname, '../../agents/venv/Scripts/python.exe');
    this.agentPath = path.join(__dirname, '../../agents/finance/finance_agent.py');
    this.tempDir = path.join(__dirname, '../temp');
    
    // Ensure temp directory exists
    this._ensureTempDir();
  }

  async _ensureTempDir() {
    try {
      await fs.mkdir(this.tempDir, { recursive: true });
    } catch (error) {
      console.error('Error creating temp directory:', error.message);
    }
  }

  /**
   * Perform comprehensive ML-powered financial analysis
   * @param {Object} financialData - Financial data from existing service
   * @param {Object} options - Analysis options
   * @returns {Promise<Object>} ML analysis results
   */
  async analyzeCompanyFinancials(financialData, options = {}) {
    try {
      console.log('[ML Financial Analysis] Starting comprehensive analysis...');
      
      // Create temporary input file
      const inputId = uuidv4();
      const inputFile = path.join(this.tempDir, `input_${inputId}.json`);
      const outputFile = path.join(this.tempDir, `output_${inputId}.json`);
      
      // Prepare input data
      const inputData = {
        action: 'comprehensive_analysis',
        financial_data: financialData,
        options: {
          forecast_years: options.forecast_years || 3,
          include_narrative_analysis: options.include_narrative_analysis !== false,
          ...options
        }
      };
      
      await fs.writeFile(inputFile, JSON.stringify(inputData, null, 2));
      
      // Execute Python ML analysis
      const result = await this._executePythonAnalysis(inputFile, outputFile);
      
      // Clean up temporary files
      await this._cleanupTempFiles([inputFile, outputFile]);
      
      console.log('[ML Financial Analysis] Comprehensive analysis completed');
      return result;
      
    } catch (error) {
      console.error('[ML Financial Analysis] Error in comprehensive analysis:', error.message);
      throw error;
    }
  }

  /**
   * Perform quick financial health check
   * @param {Object} financialData - Financial data
   * @returns {Promise<Object>} Health check results
   */
  async quickHealthCheck(financialData) {
    try {
      console.log('[ML Financial Analysis] Starting quick health check...');
      
      const inputId = uuidv4();
      const inputFile = path.join(this.tempDir, `input_${inputId}.json`);
      const outputFile = path.join(this.tempDir, `output_${inputId}.json`);
      
      const inputData = {
        action: 'quick_health_check',
        financial_data: financialData
      };
      
      await fs.writeFile(inputFile, JSON.stringify(inputData, null, 2));
      
      const result = await this._executePythonAnalysis(inputFile, outputFile);
      
      await this._cleanupTempFiles([inputFile, outputFile]);
      
      console.log('[ML Financial Analysis] Quick health check completed');
      return result;
      
    } catch (error) {
      console.error('[ML Financial Analysis] Error in quick health check:', error.message);
      throw error;
    }
  }

  /**
   * Compare multiple companies using ML analysis
   * @param {Array} companyDataList - Array of company financial data
   * @returns {Promise<Object>} Comparison results
   */
  async compareCompanies(companyDataList) {
    try {
      console.log(`[ML Financial Analysis] Starting comparison of ${companyDataList.length} companies...`);
      
      const inputId = uuidv4();
      const inputFile = path.join(this.tempDir, `input_${inputId}.json`);
      const outputFile = path.join(this.tempDir, `output_${inputId}.json`);
      
      const inputData = {
        action: 'compare_companies',
        company_data_list: companyDataList
      };
      
      await fs.writeFile(inputFile, JSON.stringify(inputData, null, 2));
      
      const result = await this._executePythonAnalysis(inputFile, outputFile);
      
      await this._cleanupTempFiles([inputFile, outputFile]);
      
      console.log('[ML Financial Analysis] Company comparison completed');
      return result;
      
    } catch (error) {
      console.error('[ML Financial Analysis] Error in company comparison:', error.message);
      throw error;
    }
  }

  /**
   * Test ML analysis capabilities
   * @returns {Promise<Object>} Test results
   */
  async testCapabilities() {
    try {
      console.log('[ML Financial Analysis] Testing capabilities...');
      
      const inputId = uuidv4();
      const inputFile = path.join(this.tempDir, `input_${inputId}.json`);
      const outputFile = path.join(this.tempDir, `output_${inputId}.json`);
      
      const inputData = {
        action: 'test_capabilities'
      };
      
      await fs.writeFile(inputFile, JSON.stringify(inputData, null, 2));
      
      const result = await this._executePythonAnalysis(inputFile, outputFile);
      
      await this._cleanupTempFiles([inputFile, outputFile]);
      
      console.log('[ML Financial Analysis] Capability test completed');
      return result;
      
    } catch (error) {
      console.error('[ML Financial Analysis] Error testing capabilities:', error.message);
      throw error;
    }
  }

  /**
   * Execute Python ML analysis
   * @param {string} inputFile - Path to input JSON file
   * @param {string} outputFile - Path to output JSON file
   * @returns {Promise<Object>} Analysis results
   * @private
   */
  async _executePythonAnalysis(inputFile, outputFile) {
    return new Promise((resolve, reject) => {
      const pythonProcess = spawn(this.pythonPath, [
        path.join(__dirname, 'mlAnalysisWrapper.py'),
        inputFile,
        outputFile
      ], {
        cwd: path.dirname(this.agentPath),
        stdio: ['pipe', 'pipe', 'pipe']
      });

      let stdout = '';
      let stderr = '';

      pythonProcess.stdout.on('data', (data) => {
        stdout += data.toString();
      });

      pythonProcess.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      pythonProcess.on('close', async (code) => {
        if (code === 0) {
          try {
            // Read the output file
            const outputData = await fs.readFile(outputFile, 'utf8');
            const result = JSON.parse(outputData);
            resolve(result);
          } catch (error) {
            reject(new Error(`Failed to read output: ${error.message}`));
          }
        } else {
          reject(new Error(`Python process failed with code ${code}: ${stderr}`));
        }
      });

      pythonProcess.on('error', (error) => {
        reject(new Error(`Failed to start Python process: ${error.message}`));
      });

      // Set timeout
      setTimeout(() => {
        pythonProcess.kill();
        reject(new Error('Python analysis timeout'));
      }, 120000); // 2 minutes timeout
    });
  }

  /**
   * Clean up temporary files
   * @param {Array} files - Array of file paths to delete
   * @private
   */
  async _cleanupTempFiles(files) {
    for (const file of files) {
      try {
        await fs.unlink(file);
      } catch (error) {
        // Ignore cleanup errors
        console.warn(`[ML Financial Analysis] Failed to cleanup ${file}:`, error.message);
      }
    }
  }

  /**
   * Check if ML analysis is available
   * @returns {Promise<boolean>} True if available
   */
  async isAvailable() {
    try {
      // Check if Python executable exists
      await fs.access(this.pythonPath);
      
      // Check if agent script exists
      await fs.access(this.agentPath);
      
      return true;
    } catch (error) {
      console.warn('[ML Financial Analysis] ML analysis not available:', error.message);
      return false;
    }
  }
}

module.exports = MLFinancialAnalysisService;