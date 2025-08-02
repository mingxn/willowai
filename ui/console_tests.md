# 🧪 Test Commands for Browser Console

## 1. Test API Connection
```javascript
fetch('http://127.0.0.1:5000/health')
  .then(r => r.json())
  .then(d => console.log('API Health:', d))
```

## 2. Test Schedule Functions (trong Vue DevTools)
```javascript
// Tạo schedule mới
this.newSchedule = {
  plantName: 'Test Plant',
  careType: 'watering',
  startDate: new Date(Date.now() + 30*60*1000).toISOString().slice(0,16),
  repeatType: 'daily',
  repeatCount: 5,
  notes: 'Test note'
};
this.createSchedule();

// Kiểm tra schedules
console.log('Current schedules:', this.careSchedules);
console.log('Upcoming reminders:', this.upcomingReminders);
```

## 3. Test Formatting Functions
```javascript
// Test care type functions
console.log(this.getCareTypeIcon('watering')); // Should return 💧
console.log(this.getCareTypeName('watering')); // Should return "Tưới nước"

// Test time formatting
const now = new Date();
const future = new Date(now.getTime() + 45*60*1000);
console.log(this.formatReminderTime(future)); // Should return "45 phút nữa"
```

## 4. Test Analysis Formatting
```javascript
const testData = {
  "1. NHẬN DẠNG CÂY": {
    "Tên khoa học và tên thông thường": {
      "Tên khoa học": "Rosa damascena",
      "Tên thông thường": "Hoa hồng Damascus"
    }
  }
};
console.log(this.formatStructuredAnalysis(testData));
```

## 5. Test LocalStorage
```javascript
// Save test data
localStorage.setItem('plantCareSchedules', JSON.stringify([{
  id: 1,
  plantName: 'Test Plant',
  careType: 'watering',
  startDate: new Date(),
  repeatType: 'daily',
  repeatCount: 3
}]));

// Load and check
this.loadSchedulesFromStorage();
console.log('Loaded schedules:', this.careSchedules);
```

## 6. Test Notifications
```javascript
// Request permission
Notification.requestPermission().then(permission => {
  console.log('Notification permission:', permission);
  if (permission === 'granted') {
    new Notification('Test from console!', {
      body: 'This is a test notification'
    });
  }
});
```

## 7. Test Error Handling
```javascript
// Test với invalid data
try {
  this.formatStructuredAnalysis(null);
} catch(e) {
  console.log('Error handled:', e.message);
}

// Test API with wrong endpoint
fetch('http://127.0.0.1:5000/invalid')
  .then(r => r.json())
  .catch(e => console.log('API error handled:', e.message));
```

## 8. Test Auto Schedule Generation
```javascript
// Test plant info extraction
const testAnalysisData = {
  "1. NHẬN DẠNG CÂY": {
    "Tên khoa học và tên thông thường": {
      "Tên khoa học": "Rosa damascena",
      "Tên thông thường": "Hoa hồng Damascus"
    }
  },
  "2. TÌNH TRẠNG SỨC KHỎE": {
    "Tình trạng tổng thể": "Khỏe mạnh"
  }
};

const plantInfo = this.extractPlantInfo('', testAnalysisData);
console.log('Extracted plant info:', plantInfo);

// Test care recommendations
const recommendations = this.generateCareRecommendations(plantInfo, testAnalysisData);
console.log('Generated recommendations:', recommendations);

// Test watering frequency determination
const wateringFreq = this.determineWateringFrequency(plantInfo);
console.log('Watering frequency:', wateringFreq);

// Test auto schedule creation
this.autoGenerateCareSchedule('Hoa hồng Test', testAnalysisData);
```

## 9. Test Schedule Details View
```javascript
// Create a test schedule first
this.newSchedule = {
  plantName: 'Hoa hồng Test Chi tiết',
  careType: 'watering',
  startDate: new Date(Date.now() + 30*60*1000).toISOString().slice(0,16),
  repeatType: 'daily',
  repeatCount: 7,
  notes: 'Test xem chi tiết lịch chăm sóc với nhiều thông tin'
};
this.createSchedule();

// Test viewing details
const testSchedule = this.careSchedules[this.careSchedules.length - 1];
this.viewScheduleDetails(testSchedule);

// Test helper functions
console.log('Schedule progress:', this.getScheduleProgress(testSchedule));
console.log('Progress percentage:', this.getProgressPercentage(testSchedule));
console.log('Next reminder:', this.getNextReminder(testSchedule));
console.log('Formatted date:', this.formatDateTime(testSchedule.startDate));

// Test duplicate function
this.duplicateSchedule(testSchedule);
```

## 10. Performance Tests
```javascript
// Test large schedule list
const largeScheduleList = Array.from({length: 100}, (_, i) => ({
  id: i + 1,
  plantName: `Plant ${i + 1}`,
  careType: 'watering',
  startDate: new Date(Date.now() + i * 60 * 60 * 1000),
  repeatType: 'daily',
  repeatCount: 10
}));

console.time('Large list processing');
localStorage.setItem('plantCareSchedules', JSON.stringify(largeScheduleList));
this.loadSchedulesFromStorage();
console.log('Upcoming from large list:', this.upcomingReminders.length);
console.timeEnd('Large list processing');
```
