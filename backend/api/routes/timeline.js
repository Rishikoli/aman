const express = require('express');
const router = express.Router();
const timelinePrediction = require('../../services/timelinePrediction');

/**
 * Calculate timeline estimate for a deal
 * POST /api/timeline/calculate/:dealId
 */
router.post('/calculate/:dealId', async (req, res) => {
  try {
    const { dealId } = req.params;
    const { documentData, externalMilestones } = req.body;

    const timeline = await timelinePrediction.calculateTimeline(
      dealId, 
      documentData || {}, 
      externalMilestones || []
    );

    res.json({
      success: true,
      data: timeline
    });
  } catch (error) {
    console.error('Timeline calculation error:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * Update timeline with real-time progress
 * PUT /api/timeline/update/:dealId
 */
router.put('/update/:dealId', async (req, res) => {
  try {
    const { dealId } = req.params;

    const updatedTimeline = await timelinePrediction.updateTimelineProgress(dealId);

    res.json({
      success: true,
      data: updatedTimeline
    });
  } catch (error) {
    console.error('Timeline update error:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * Get current timeline estimate for a deal
 * GET /api/timeline/:dealId
 */
router.get('/:dealId', async (req, res) => {
  try {
    const { dealId } = req.params;

    const timeline = await timelinePrediction.getStoredTimelineEstimate(dealId);

    if (!timeline) {
      return res.status(404).json({
        success: false,
        error: 'Timeline estimate not found for this deal'
      });
    }

    res.json({
      success: true,
      data: timeline
    });
  } catch (error) {
    console.error('Timeline retrieval error:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * Get timeline history for a deal
 * GET /api/timeline/:dealId/history
 */
router.get('/:dealId/history', async (req, res) => {
  try {
    const { dealId } = req.params;

    const history = await timelinePrediction.getTimelineHistory(dealId);

    res.json({
      success: true,
      data: history
    });
  } catch (error) {
    console.error('Timeline history error:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * Analyze document complexity
 * POST /api/timeline/analyze-complexity
 */
router.post('/analyze-complexity', async (req, res) => {
  try {
    const { documentData } = req.body;

    if (!documentData) {
      return res.status(400).json({
        success: false,
        error: 'Document data is required'
      });
    }

    const complexityAnalysis = timelinePrediction.analyzeDocumentComplexity(documentData);

    res.json({
      success: true,
      data: complexityAnalysis
    });
  } catch (error) {
    console.error('Complexity analysis error:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * Get timeline predictions for multiple deals
 * GET /api/timeline/batch
 */
router.get('/batch', async (req, res) => {
  try {
    const { dealIds } = req.query;

    if (!dealIds) {
      return res.status(400).json({
        success: false,
        error: 'Deal IDs are required'
      });
    }

    const dealIdArray = Array.isArray(dealIds) ? dealIds : dealIds.split(',');
    const timelines = [];

    for (const dealId of dealIdArray) {
      try {
        const timeline = await timelinePrediction.getStoredTimelineEstimate(dealId.trim());
        if (timeline) {
          timelines.push(timeline);
        }
      } catch (error) {
        console.error(`Error getting timeline for deal ${dealId}:`, error);
        // Continue with other deals
      }
    }

    res.json({
      success: true,
      data: timelines
    });
  } catch (error) {
    console.error('Batch timeline retrieval error:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

module.exports = router;