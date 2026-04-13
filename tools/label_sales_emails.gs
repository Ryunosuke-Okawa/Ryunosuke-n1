/**
 * 営業メール自動振り分けスクリプト
 * 9時・15時・21時に自動実行
 * Google Apps Script (script.google.com) で使用
 */

// 信頼済みドメイン（振り分け除外）
var TRUSTED_DOMAINS = [
  'n1-inc.co.jp',
  'kirin.co.jp',
  'shimz.co.jp',
  'ntt-nexia.co.jp',
  'gmo-pg.com',
  'accounts.google.com',
  'google.com',
];

// 営業メールのラベル名
var LABEL_NAME = '営業メール';

function labelSalesEmails() {
  var label = GmailApp.getUserLabelByName(LABEL_NAME);
  if (!label) {
    label = GmailApp.createLabel(LABEL_NAME);
    Logger.log('ラベル「' + LABEL_NAME + '」を新規作成しました');
  }

  // 除外ドメインのフィルタ文字列を生成
  var excludeQuery = TRUSTED_DOMAINS.map(function(d) {
    return '-from:@' + d;
  }).join(' ');

  // 検索クエリ（受信トレイ内の営業メール候補）
  var queries = [
    // プロモーションカテゴリ
    'in:inbox category:promotions ' + excludeQuery,
    // アップデートカテゴリ内の営業系キーワード
    'in:inbox category:updates (ウェビナー OR セミナー OR メルマガ OR 資料請求 OR お申し込み OR ご招待 OR 【無料) ' + excludeQuery,
  ];

  var processedIds = {};
  var totalCount = 0;

  queries.forEach(function(query) {
    var threads = GmailApp.search(query, 0, 100);
    threads.forEach(function(thread) {
      var id = thread.getId();
      if (!processedIds[id]) {
        processedIds[id] = true;
        thread.addLabel(label);
        thread.moveToArchive(); // 受信トレイから除外
        totalCount++;
      }
    });
  });

  Logger.log('[' + new Date().toLocaleString('ja-JP') + '] 処理完了: ' + totalCount + '件のスレッドを「営業メール」に移動');
}

/**
 * トリガーを自動設定する関数
 * 初回のみ手動で実行してください（スクリプトエディタの▶ボタン）
 */
function setupTriggers() {
  // 既存のトリガーを全削除（重複防止）
  ScriptApp.getProjectTriggers().forEach(function(trigger) {
    if (trigger.getHandlerFunction() === 'labelSalesEmails') {
      ScriptApp.deleteTrigger(trigger);
    }
  });

  // 9時トリガー
  ScriptApp.newTrigger('labelSalesEmails')
    .timeBased()
    .atHour(9)
    .everyDays(1)
    .inTimezone('Asia/Tokyo')
    .create();

  // 15時トリガー
  ScriptApp.newTrigger('labelSalesEmails')
    .timeBased()
    .atHour(15)
    .everyDays(1)
    .inTimezone('Asia/Tokyo')
    .create();

  // 21時トリガー
  ScriptApp.newTrigger('labelSalesEmails')
    .timeBased()
    .atHour(21)
    .everyDays(1)
    .inTimezone('Asia/Tokyo')
    .create();

  Logger.log('トリガー設定完了: 毎日 9時・15時・21時 (Asia/Tokyo)');
}
