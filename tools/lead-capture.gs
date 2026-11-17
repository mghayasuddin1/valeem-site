/**
 * Valeem lead capture: Google Sheet + email alert.
 * Used by both the homepage demo form and the Homeschool Pathways consultation form.
 * Lives in Apps Script, attached to the "Homeschool Pathways Enquiries" Sheet.
 * This copy is for reference; editing it here does NOT change the live script.
 *
 * To update the live script: paste this file into Apps Script, save, then
 * Deploy > Manage deployments > pencil > Version: New version > Deploy (keeps the same URL).
 */

var SHEET_ID      = 'PASTE_SHEET_ID_HERE';   // the long ID in the Sheet's address bar, between /d/ and /edit
var NOTIFY_EMAILS = 'contact@valeem.com';   // comma-separate more addresses if needed
var SHEET_NAME    = 'Enquiries';

var COLUMNS = [
  'submitted_at', 'parent_name', 'phone', 'email', 'city_country',
  'child_age', 'homeschooled', 'background', 'homeschool_duration',
  'interests', 'message', 'consent',
  'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term',
  'landing_page', 'referrer'
];

function saveEnquiry(p) {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var sheet = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(['received_at'].concat(COLUMNS).concat(['status', 'counsellor_notes']));
    sheet.setFrozenRows(1);
  }
  var row = [new Date()].concat(COLUMNS.map(function (k) {
    var v = String(p[k] || '');
    return /^[=+\-@]/.test(v) ? "'" + v : v;
  })).concat(['New', '']);
  sheet.appendRow(row);

  var source = p.utm_source ? (p.utm_source + ' / ' + (p.utm_medium || '-') + ' / ' + (p.utm_campaign || '-')) : 'Direct or organic (no UTM)';
  var body = [
    'New enquiry from valeem.com.', '',
    'Parent: ' + (p.parent_name || ''),
    'Phone/WhatsApp: ' + (p.phone || ''),
    'Email: ' + (p.email || '-'),
    'City/country: ' + (p.city_country || ''), '',
    "Child's age: " + (p.child_age || '-'),
    'Currently homeschooled: ' + (p.homeschooled || '-'),
    'Background: ' + (p.background || '-'),
    'Homeschooling for: ' + (p.homeschool_duration || '-'),
    'Interested in: ' + (p.interests || '-'), '',
    'Message: ' + (p.message || '-'), '',
    'Source: ' + source,
    'Landing page: ' + (p.landing_page || '-'),
    'Referrer: ' + (p.referrer || '-'), '',
    'Sheet: ' + ss.getUrl()
  ].join('\n');
  MailApp.sendEmail({
    to: NOTIFY_EMAILS,
    subject: 'Valeem enquiry: ' + (p.parent_name || 'New parent') + (p.interests ? ' (' + p.interests + ')' : ''),
    body: body
  });
}

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    saveEnquiry((e && e.parameter) || {});
    return ContentService.createTextOutput(JSON.stringify({ ok: true })).setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    console.error('Enquiry failed: ' + err);
    return ContentService.createTextOutput(JSON.stringify({ ok: false, error: String(err) })).setMimeType(ContentService.MimeType.JSON);
  } finally {
    lock.releaseLock();
  }
}

function doGet() {
  return ContentService.createTextOutput('Valeem Homeschool Pathways lead endpoint is running.');
}

// Run once from the editor to grant permissions and confirm the Sheet and email work.
function testSetup() {
  saveEnquiry({ parent_name: 'TEST from script', phone: '0300 0000000', city_country: 'Karachi, Pakistan', child_age: '8', homeschooled: 'Yes', message: 'Setup test, please ignore', consent: 'on' });
}
