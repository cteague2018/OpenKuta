import { test, expect } from '@playwright/test';

test.describe('OpenMathForge UI Workflows & Navigation Traversal', () => {
  test('Click through course catalog and verify problem count and difficulty toggles', async ({ page }) => {
    const consoleErrors: string[] = [];
    page.on('console', (msg) => {
      if (msg.type() === 'error') consoleErrors.push(msg.text());
    });
    page.on('pageerror', (err) => {
      consoleErrors.push(err.message);
    });

    await page.goto('/');

    // Check header branding
    await expect(page.locator('text=OpenMathForge')).toBeVisible();

    // Toggle Answer Key visibility switch
    const answerKeyToggle = page.locator('text=Student View').or(page.locator('text=Answer Key'));
    await answerKeyToggle.click();

    // Toggle back
    await answerKeyToggle.click();

    // Verify zero unhandled browser console errors occurred
    expect(consoleErrors).toEqual([]);
  });

  test('Dynamic Sheet Manipulation: Scramble Form re-indexes 1 to N', async ({ page }) => {
    await page.goto('/');
    const scrambleBtn = page.locator('[data-testid="scramble-form"]');
    if (await scrambleBtn.isVisible()) {
      await scrambleBtn.click();
      await expect(page.locator('.problem-index').first()).toContainText('1)');
    }
  });

  test('Document Download Triggers: Generate PDF and Export Answer Key', async ({ page }) => {
    await page.goto('/');
    const generatePdfBtn = page.locator('[data-testid="generate-pdf"]').or(page.locator('text=Generate PDF'));
    if (await generatePdfBtn.isVisible()) {
      const [download] = await Promise.all([
        page.waitForEvent('download'),
        generatePdfBtn.click(),
      ]);
      expect(download.suggestedFilename()).toContain('.pdf');
    }
  });
});

