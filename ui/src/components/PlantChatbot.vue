<template>
  <div>
    <div class="chat-container">
      <!-- Sidebar -->
      <div class="sidebar">
        <div class="logo">
          <h1>🌿 Plant AI</h1>
          <p>Chatbot phân tích cây trồng</p>
        </div>

        <div class="chat-info">
          <h3><i class="fas fa-info-circle"></i> Tính năng</h3>
          <ul>
            <li>Nhận dạng cây trồng</li>
            <li>Phát hiện bệnh</li>
            <li>Phân tích sinh trưởng</li>
            <li>Khuyến nghị chăm sóc</li>
            <li>Tư vấn trực tiếp</li>
            <li>Lịch chăm sóc cây</li>
          </ul>
        </div>

        <div class="chat-info">
          <h3><i class="fas fa-calendar-alt"></i> Lịch chăm sóc</h3>
          <div class="schedule-stats">
            <p>
              <strong>{{ careSchedules.length }}</strong> lịch đã tạo
            </p>
            <p>
              <strong>{{ upcomingReminders.length }}</strong> nhắc nhở sắp tới
            </p>
          </div>
          <button @click="showScheduleModal = true" class="create-schedule-btn">
            <i class="fas fa-plus"></i> Tạo lịch mới
          </button>
          <button @click="showScheduleList = true" class="view-schedule-btn">
            <i class="fas fa-calendar-check"></i> Xem lịch
          </button>
        </div>

        <div class="chat-info">
          <h3><i class="fas fa-image"></i> Hỗ trợ định dạng</h3>
          <ul>
            <li>JPG, JPEG</li>
            <li>PNG, WEBP</li>
            <li>Tối đa 10MB</li>
          </ul>
        </div>

        <div class="chat-info">
          <h3><i class="fas fa-clock"></i> Trạng thái API</h3>
          <ul>
            <li v-if="apiStatus.connected" style="color: #2ecc71">
              <i class="fas fa-check-circle"></i> Đã kết nối
            </li>
            <li v-else style="color: #e74c3c">
              <i class="fas fa-times-circle"></i> Mất kết nối
            </li>
          </ul>
        </div>
      </div>

      <!-- Main Chat -->
      <div class="main-chat">
        <div class="chat-header">
          <h2>💬 Chatbot Phân Tích Cây Trồng</h2>
          <p>Gửi hình ảnh cây của bạn và đặt câu hỏi để nhận tư vấn</p>
        </div>

        <div class="chat-messages" ref="messagesContainer">
          <!-- Welcome message -->
          <div class="message bot" v-if="messages.length === 0">
            <div class="message-content">
              <strong>👋 Chào mừng bạn đến với Plant Analysis AI!</strong
              ><br /><br />
              Tôi có thể giúp bạn:
              <ul style="margin: 10px 0; padding-left: 20px">
                <li>📸 Phân tích hình ảnh cây trồng</li>
                <li>🔍 Nhận dạng loại cây</li>
                <li>🩺 Chẩn đoán bệnh trên cây</li>
                <li>📈 Đánh giá tình trạng sinh trưởng</li>
                <li>💡 Đưa ra khuyến nghị chăm sóc</li>
                <li>🤖 <strong>Tự động tạo lịch chăm sóc</strong></li>
              </ul>
              <div
                style="
                  background: #e8f5e8;
                  padding: 10px;
                  border-radius: 8px;
                  margin-top: 10px;
                  border-left: 4px solid #2ecc71;
                "
              >
                <strong>🆕 Tính năng mới:</strong> Sau khi phân tích hình ảnh,
                tôi sẽ tự động đề xuất và tạo lịch chăm sóc phù hợp với từng
                loại cây!
              </div>
              <br />
              Hãy gửi hình ảnh cây của bạn hoặc đặt câu hỏi để bắt đầu!
            </div>
          </div>

          <!-- Chat messages -->
          <div
            v-for="message in messages"
            :key="message.id"
            :class="['message', message.type]"
          >
            <div class="message-content">
              <div v-if="message.image" class="image-preview">
                <img :src="message.image" alt="Uploaded image" />
              </div>

              <div v-html="message.content"></div>

              <div v-if="message.analysis" class="analysis-result">
                <div
                  class="analysis-section"
                  v-if="message.analysis.plant_info"
                >
                  <h4><i class="fas fa-seedling"></i> Nhận dạng cây</h4>
                  <p>
                    <strong>Tên khoa học:</strong>
                    {{
                      message.analysis.plant_info.scientific_name ||
                      "Chưa xác định"
                    }}
                  </p>
                  <p>
                    <strong>Tên thông thường:</strong>
                    {{
                      message.analysis.plant_info.common_name || "Chưa xác định"
                    }}
                  </p>
                  <p>
                    <strong>Độ tin cậy:</strong>
                    {{ message.analysis.plant_info.confidence || "N/A" }}%
                  </p>
                </div>

                <div
                  class="analysis-section"
                  v-if="message.analysis.health_status"
                >
                  <h4><i class="fas fa-heartbeat"></i> Tình trạng sức khỏe</h4>
                  <p>
                    <strong>Trạng thái:</strong>
                    {{ message.analysis.health_status.overall_status }}
                  </p>
                  <p v-if="message.analysis.health_status.severity_level">
                    <strong>Mức độ:</strong>
                    {{ message.analysis.health_status.severity_level }}
                  </p>
                </div>

                <div
                  class="analysis-section"
                  v-if="message.analysis.recommendations"
                >
                  <h4><i class="fas fa-lightbulb"></i> Khuyến nghị</h4>
                  <ul v-if="message.analysis.recommendations.treatment_steps">
                    <li
                      v-for="step in message.analysis.recommendations
                        .treatment_steps"
                      :key="step"
                    >
                      {{ step }}
                    </li>
                  </ul>
                </div>
              </div>

              <div class="message-time">
                {{ formatTime(message.timestamp) }}
              </div>
            </div>
          </div>

          <!-- Typing indicator -->
          <div v-if="isTyping" class="typing-indicator">
            <div class="typing-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <span class="typing-text">Đang phân tích...</span>
          </div>
        </div>

        <!-- Chat Input -->
        <div class="chat-input-container">
          <div v-if="errorMessage" class="error-message">
            <i class="fas fa-exclamation-triangle"></i> {{ errorMessage }}
          </div>

          <div v-if="successMessage" class="success-message">
            <i class="fas fa-check"></i> {{ successMessage }}
          </div>

          <div class="chat-input-wrapper">
            <div class="image-upload">
              <input
                type="file"
                id="imageInput"
                @change="handleImageUpload"
                accept="image/*"
              />
              <label
                for="imageInput"
                :class="{ 'has-image': selectedImage }"
                :title="selectedImage ? 'Đã chọn hình ảnh' : 'Upload hình ảnh'"
              >
                <i
                  :class="selectedImage ? 'fas fa-check' : 'fas fa-camera'"
                ></i>
              </label>
            </div>
            <textarea
              v-model="currentMessage"
              @keydown="handleKeydown"
              placeholder="Gửi hình ảnh hoặc đặt câu hỏi về cây trồng..."
              class="chat-input"
              :disabled="isTyping"
            ></textarea>

            <button
              @click="sendMessage"
              :disabled="isTyping || (!currentMessage.trim() && !selectedImage)"
              class="send-button"
              title="Gửi tin nhắn"
            >
              <i class="fas fa-paper-plane"></i>
            </button>
          </div>
        </div>
      </div>

      <!-- Schedule Modal -->
      <div
        v-if="showScheduleModal"
        class="modal-overlay"
        @click="closeScheduleModal"
      >
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h3><i class="fas fa-calendar-plus"></i> Tạo lịch chăm sóc cây</h3>
            <button @click="showScheduleModal = false" class="close-btn">
              <i class="fas fa-times"></i>
            </button>
          </div>

          <div class="modal-body">
            <div class="form-group">
              <label><i class="fas fa-seedling"></i> Tên cây:</label>
              <input
                v-model="newSchedule.plantName"
                type="text"
                placeholder="VD: Cây hoa hồng"
              />
            </div>

            <div class="form-group">
              <label><i class="fas fa-tasks"></i> Loại chăm sóc:</label>
              <select v-model="newSchedule.careType">
                <option value="watering">💧 Tưới nước</option>
                <option value="fertilizing">🌱 Bón phân</option>
                <option value="pruning">✂️ Tỉa cành</option>
                <option value="repotting">🪴 Thay chậu</option>
                <option value="spraying">💨 Phun thuốc</option>
                <option value="checking">🔍 Kiểm tra sức khỏe</option>
              </select>
            </div>

            <div class="form-group">
              <label><i class="fas fa-clock"></i> Thời gian bắt đầu:</label>
              <input v-model="newSchedule.startDate" type="datetime-local" />
            </div>

            <div class="form-group">
              <label><i class="fas fa-redo"></i> Lặp lại:</label>
              <select v-model="newSchedule.repeatType">
                <option value="none">Không lặp lại</option>
                <option value="daily">Hàng ngày</option>
                <option value="weekly">Hàng tuần</option>
                <option value="monthly">Hàng tháng</option>
              </select>
            </div>

            <div v-if="newSchedule.repeatType !== 'none'" class="form-group">
              <label><i class="fas fa-hashtag"></i> Số lần lặp:</label>
              <input
                v-model="newSchedule.repeatCount"
                type="number"
                min="1"
                max="365"
                placeholder="VD: 30"
              />
            </div>

            <div class="form-group">
              <label><i class="fas fa-sticky-note"></i> Ghi chú:</label>
              <textarea
                v-model="newSchedule.notes"
                placeholder="Ghi chú thêm về cách chăm sóc..."
              ></textarea>
            </div>
          </div>

          <div class="modal-footer">
            <button @click="showScheduleModal = false" class="btn-secondary">
              <i class="fas fa-times"></i> Hủy
            </button>
            <button
              @click="createSchedule"
              class="btn-primary"
              :disabled="!isScheduleValid"
            >
              <i class="fas fa-save"></i> Tạo lịch
            </button>
          </div>
        </div>
      </div>

      <!-- Schedule List Modal -->
      <div
        v-if="showScheduleList"
        class="modal-overlay"
        @click="closeScheduleList"
      >
        <div class="modal-content schedule-list-modal" @click.stop>
          <div class="modal-header">
            <h3><i class="fas fa-calendar-check"></i> Lịch chăm sóc của bạn</h3>
            <button @click="showScheduleList = false" class="close-btn">
              <i class="fas fa-times"></i>
            </button>
          </div>

          <div class="modal-body">
            <div class="schedule-tabs">
              <button
                :class="['tab-btn', { active: activeTab === 'upcoming' }]"
                @click="activeTab = 'upcoming'"
              >
                <i class="fas fa-clock"></i> Sắp tới ({{
                  upcomingReminders.length
                }})
              </button>
              <button
                :class="['tab-btn', { active: activeTab === 'all' }]"
                @click="activeTab = 'all'"
              >
                <i class="fas fa-list"></i> Tất cả ({{ careSchedules.length }})
              </button>
            </div>

            <div class="schedule-content">
              <div v-if="activeTab === 'upcoming'" class="upcoming-reminders">
                <div v-if="upcomingReminders.length === 0" class="empty-state">
                  <i class="fas fa-calendar-times"></i>
                  <p>Không có nhắc nhở nào sắp tới</p>
                </div>
                <div v-else>
                  <div
                    v-for="reminder in upcomingReminders"
                    :key="reminder.id"
                    class="reminder-item urgent"
                  >
                    <div class="reminder-icon">
                      {{ getCareTypeIcon(reminder.careType) }}
                    </div>
                    <div class="reminder-info">
                      <h4>{{ reminder.plantName }}</h4>
                      <p>{{ getCareTypeName(reminder.careType) }}</p>
                      <span class="reminder-time">{{
                        formatReminderTime(reminder.nextDate)
                      }}</span>
                    </div>
                    <button @click="markAsDone(reminder.id)" class="done-btn">
                      <i class="fas fa-check"></i>
                    </button>
                  </div>
                </div>
              </div>

              <div v-if="activeTab === 'all'" class="all-schedules">
                <div v-if="careSchedules.length === 0" class="empty-state">
                  <i class="fas fa-seedling"></i>
                  <p>Chưa có lịch chăm sóc nào</p>
                  <button
                    @click="
                      showScheduleModal = true;
                      showScheduleList = false;
                    "
                    class="btn-primary"
                  >
                    <i class="fas fa-plus"></i> Tạo lịch đầu tiên
                  </button>
                </div>
                <div v-else>
                  <div
                    v-for="schedule in careSchedules"
                    :key="schedule.id"
                    class="schedule-item"
                  >
                    <div class="schedule-icon">
                      {{ getCareTypeIcon(schedule.careType) }}
                    </div>
                    <div class="schedule-info">
                      <h4>
                        {{ schedule.plantName }}
                        <span v-if="schedule.autoGenerated" class="auto-badge"
                          >🤖 AI</span
                        >
                      </h4>
                      <p>{{ getCareTypeName(schedule.careType) }}</p>
                      <span class="schedule-repeat">{{
                        getRepeatText(schedule)
                      }}</span>
                      <p v-if="schedule.notes" class="schedule-notes">
                        {{ schedule.notes }}
                      </p>
                    </div>
                    <div class="schedule-actions">
                      <button
                        @click="viewScheduleDetails(schedule)"
                        class="view-btn"
                        title="Xem chi tiết"
                      >
                        <i class="fas fa-eye"></i>
                      </button>
                      <button
                        @click="editSchedule(schedule)"
                        class="edit-btn"
                        title="Chỉnh sửa"
                      >
                        <i class="fas fa-edit"></i>
                      </button>
                      <button
                        @click="deleteSchedule(schedule.id)"
                        class="delete-btn"
                        title="Xóa"
                      >
                        <i class="fas fa-trash"></i>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Chi tiết Lịch -->
    <div
      v-if="showScheduleDetails"
      class="modal-overlay"
      @click="closeScheduleDetails"
    >
      <div class="modal-content schedule-details-modal" @click.stop>
        <div class="modal-header">
          <h3>📅 Chi tiết Lịch Chăm sóc</h3>
          <button @click="showScheduleDetails = false" class="close-btn">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body" v-if="selectedSchedule">
          <div class="schedule-detail-section">
            <div class="detail-item">
              <label>🌱 Tên cây:</label>
              <span class="detail-value">{{ selectedSchedule.plantName }}</span>
              <span v-if="selectedSchedule.autoGenerated" class="auto-badge"
                >🤖 AI</span
              >
            </div>

            <div class="detail-item">
              <label>🔧 Loại chăm sóc:</label>
              <span class="detail-value">
                {{ getCareTypeIcon(selectedSchedule.careType) }}
                {{ getCareTypeName(selectedSchedule.careType) }}
              </span>
            </div>

            <div class="detail-item">
              <label>📅 Ngày bắt đầu:</label>
              <span class="detail-value">{{
                formatDateTime(selectedSchedule.startDate)
              }}</span>
            </div>

            <div class="detail-item">
              <label>🔄 Lặp lại:</label>
              <span class="detail-value">{{
                getRepeatText(selectedSchedule)
              }}</span>
            </div>

            <div class="detail-item" v-if="selectedSchedule.repeatCount">
              <label>🔢 Số lần lặp:</label>
              <span class="detail-value"
                >{{ selectedSchedule.repeatCount }} lần</span
              >
            </div>

            <div class="detail-item" v-if="selectedSchedule.notes">
              <label>📝 Ghi chú:</label>
              <span class="detail-value notes-text">{{
                selectedSchedule.notes
              }}</span>
            </div>

            <div class="detail-item">
              <label>⏰ Trạng thái:</label>
              <span class="detail-value status-active">Đang hoạt động</span>
            </div>

            <div class="detail-item">
              <label>📊 Tiến độ:</label>
              <div class="progress-info">
                <span class="detail-value">{{
                  getScheduleProgress(selectedSchedule)
                }}</span>
                <div class="progress-bar">
                  <div
                    class="progress-fill"
                    :style="{
                      width: getProgressPercentage(selectedSchedule) + '%',
                    }"
                  ></div>
                </div>
              </div>
            </div>

            <div class="detail-item" v-if="getNextReminder(selectedSchedule)">
              <label>⏰ Nhắc nhở tiếp theo:</label>
              <span class="detail-value next-reminder">
                {{ formatDateTime(getNextReminder(selectedSchedule)) }}
                <small
                  >({{
                    formatReminderTime(getNextReminder(selectedSchedule))
                  }})</small
                >
              </span>
            </div>
          </div>

          <div class="schedule-actions-detail">
            <button @click="editSchedule(selectedSchedule)" class="btn-primary">
              <i class="fas fa-edit"></i> Chỉnh sửa
            </button>
            <button
              @click="duplicateSchedule(selectedSchedule)"
              class="btn-secondary"
            >
              <i class="fas fa-copy"></i> Sao chép
            </button>
            <button
              @click="deleteSchedule(selectedSchedule.id)"
              class="btn-danger"
            >
              <i class="fas fa-trash"></i> Xóa
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";

export default {
  name: "PlantChatbot",
  data() {
    return {
      messages: [],
      currentMessage: "",
      selectedImage: null,
      selectedImageFile: null,
      isTyping: false,
      errorMessage: "",
      successMessage: "",
      apiStatus: {
        connected: false,
      },
      messageId: 1,
      apiBaseUrl: "http://127.0.0.1:8000",

      // Schedule management
      showScheduleModal: false,
      showScheduleList: false,
      showScheduleDetails: false,
      selectedSchedule: null,
      activeTab: "upcoming",
      careSchedules: [],
      newSchedule: {
        plantName: "",
        careType: "watering",
        startDate: "",
        repeatType: "none",
        repeatCount: 1,
        notes: "",
      },
      scheduleIdCounter: 1,
      reminderCheckInterval: null,
    };
  },
  computed: {
    upcomingReminders() {
      const now = new Date();
      const next24Hours = new Date(now.getTime() + 24 * 60 * 60 * 1000);

      return this.careSchedules
        .filter((schedule) => {
          const nextDate = this.getNextReminderDate(schedule);
          return nextDate && nextDate <= next24Hours && nextDate >= now;
        })
        .map((schedule) => ({
          ...schedule,
          nextDate: this.getNextReminderDate(schedule),
        }))
        .sort((a, b) => a.nextDate - b.nextDate);
    },

    isScheduleValid() {
      return (
        this.newSchedule.plantName.trim() &&
        this.newSchedule.startDate &&
        this.newSchedule.careType
      );
    },
  },
  mounted() {
    this.checkApiStatus();
    this.scrollToBottom();
    this.loadSchedulesFromStorage();
    this.setupReminderCheck();
    this.setDefaultStartDate();
    this.requestNotificationPermission();
  },
  beforeUnmount() {
    if (this.reminderCheckInterval) {
      clearInterval(this.reminderCheckInterval);
    }
  },
  methods: {
    async checkApiStatus() {
      try {
        const response = await axios.get(`${this.apiBaseUrl}/health`);
        this.apiStatus.connected = response.data.status === "healthy";
      } catch (error) {
        this.apiStatus.connected = false;
      }
    },

    handleImageUpload(event) {
      const file = event.target.files[0];
      if (file) {
        // Validate file size (10MB)
        if (file.size > 10 * 1024 * 1024) {
          this.showError("File quá lớn. Vui lòng chọn file nhỏ hơn 10MB.");
          return;
        }

        // Validate file type
        const allowedTypes = [
          "image/jpeg",
          "image/jpg",
          "image/png",
          "image/webp",
        ];
        if (!allowedTypes.includes(file.type)) {
          this.showError(
            "Định dạng file không được hỗ trợ. Vui lòng chọn JPG, PNG hoặc WEBP."
          );
          return;
        }

        this.selectedImageFile = file;

        // Create preview
        const reader = new FileReader();
        reader.onload = (e) => {
          this.selectedImage = e.target.result;
        };
        reader.readAsDataURL(file);

        this.showSuccess("Đã chọn hình ảnh. Nhấn gửi để phân tích.");
      }
    },

    handleKeydown(event) {
      if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        this.sendMessage();
      }
    },

    async sendMessage() {
      if (this.isTyping) return;

      // Validate input
      if (!this.currentMessage.trim() && !this.selectedImage) {
        this.showError("Vui lòng nhập tin nhắn hoặc chọn hình ảnh.");
        return;
      }

      // Clear previous messages
      this.clearMessages();

      // Add user message
      const userMessage = {
        id: this.messageId++,
        type: "user",
        content: this.currentMessage || "Phân tích hình ảnh này",
        image: this.selectedImage,
        timestamp: new Date(),
      };
      this.messages.push(userMessage);

      // Clear input
      const messageToSend = this.currentMessage;
      const imageToSend = this.selectedImageFile;
      this.currentMessage = "";
      this.selectedImage = null;
      this.selectedImageFile = null;
      document.getElementById("imageInput").value = "";

      this.scrollToBottom();

      // Show typing indicator
      this.isTyping = true;

      try {
        let botResponse;

        if (imageToSend) {
          // Analyze image
          botResponse = await this.analyzeImage(imageToSend);
        } else {
          // Text-only message
          botResponse = await this.handleTextMessage(messageToSend);
        }

        // Add bot response
        const botMessage = {
          id: this.messageId++,
          type: "bot",
          content: botResponse.content,
          analysis: botResponse.analysis,
          timestamp: new Date(),
        };
        this.messages.push(botMessage);

        // Auto-generate care schedule if image analysis was successful
        if (imageToSend && botResponse.analysis && botResponse.plantInfo) {
          await this.autoGenerateCareSchedule(
            botResponse.plantInfo,
            botResponse.analysis
          );
        }
      } catch (error) {
        console.error("Error:", error);
        const errorMessage = {
          id: this.messageId++,
          type: "bot",
          content:
            "❌ Xin lỗi, đã xảy ra lỗi khi xử lý yêu cầu của bạn. Vui lòng thử lại.",
          timestamp: new Date(),
        };
        this.messages.push(errorMessage);
      } finally {
        this.isTyping = false;
        this.scrollToBottom();
      }
    },

    async analyzeImage(imageFile) {
      const formData = new FormData();
      formData.append("file", imageFile);
      formData.append("enhance_image", "true");

      const response = await axios.post(
        `${this.apiBaseUrl}/analyze/complete`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      const result = response.data;

      if (result.success) {
        // Parse and format the analysis text properly
        let analysisContent = "";

        if (result.analysis_text) {
          // Try to extract JSON from analysis_text
          let jsonMatch = result.analysis_text.match(
            /```json\s*([\s\S]*?)\s*```/
          );
          if (jsonMatch) {
            try {
              const jsonData = JSON.parse(jsonMatch[1]);
              analysisContent = this.formatStructuredAnalysis(jsonData);
            } catch (e) {
              // If JSON parsing fails, format as text
              analysisContent = this.formatAnalysisText(result.analysis_text);
            }
          } else {
            analysisContent = this.formatAnalysisText(result.analysis_text);
          }
        } else {
          analysisContent = "Không thể phân tích được hình ảnh này.";
        }

        return {
          content: analysisContent,
          analysis: result.structured_data,
          plantInfo: this.extractPlantInfo(
            result.analysis_text,
            result.structured_data
          ),
        };
      } else {
        throw new Error(result.error || "Phân tích thất bại");
      }
    },

    formatStructuredAnalysis(data) {
      let formatted = "📊 <strong>Kết quả phân tích chi tiết:</strong><br><br>";

      // Process each section
      for (const [key, value] of Object.entries(data)) {
        const sectionNumber = key.match(/^\d+/);

        if (key.includes("NHẬN DẠNG") || key.includes("1.")) {
          formatted += "🔍 <strong>NHẬN DẠNG CÂY</strong><br>";
          formatted += this.formatPlantIdentification(value) + "<br>";
        } else if (key.includes("TÌNH TRẠNG") || key.includes("2.")) {
          formatted += "⚕️ <strong>TÌNH TRẠNG SỨC KHỎE</strong><br>";
          formatted += this.formatHealthStatus(value) + "<br>";
        } else if (key.includes("SINH TRƯỞNG") || key.includes("3.")) {
          formatted += "📈 <strong>PHÂN TÍCH SINH TRƯỞNG</strong><br>";
          formatted += this.formatGrowthAnalysis(value) + "<br>";
        } else if (key.includes("KHUYẾN NGHỊ") || key.includes("4.")) {
          formatted += "💡 <strong>KHUYẾN NGHỊ CHĂM SÓC</strong><br>";
          formatted += this.formatRecommendations(value) + "<br>";
        } else if (key.includes("THÔNG TIN") || key.includes("5.")) {
          formatted += "📋 <strong>THÔNG TIN BỔ SUNG</strong><br>";
          formatted += this.formatAdditionalInfo(value) + "<br>";
        }
      }

      return formatted;
    },

    async handleTextMessage(message) {
      // Simple text responses for common questions
      const lowerMessage = message.toLowerCase();

      if (lowerMessage.includes("cây") || lowerMessage.includes("trồng")) {
        return {
          content: `🌱 Tôi hiểu bạn muốn hỏi về cây trồng. Để tôi có thể giúp bạn tốt nhất, hãy gửi hình ảnh cây mà bạn quan tâm. 
          
          Tôi có thể:
          • 📸 Phân tích hình ảnh để nhận dạng loại cây
          • 🔍 Phát hiện các vấn đề về sức khỏe
          • 💡 Đưa ra khuyến nghị chăm sóc cụ thể
          
          Nhấn vào icon 📷 để upload hình ảnh nhé!`,
        };
      }

      if (
        lowerMessage.includes("lịch") ||
        lowerMessage.includes("nhắc nhở") ||
        lowerMessage.includes("chăm sóc")
      ) {
        return {
          content: `📅 Tôi có thể giúp bạn tạo lịch chăm sóc cây!
        
        Các tính năng lịch chăm sóc:
        • ⏰ Đặt nhắc nhở tưới nước, bón phân
        • 🔄 Lặp lại theo chu kỳ (hàng ngày, tuần, tháng)
        • 📝 Ghi chú chi tiết cho từng hoạt động
        • 🔔 Thông báo khi đến giờ chăm sóc
        
        Nhấn nút "Tạo lịch mới" ở sidebar để bắt đầu!
        
        Hoặc hỏi tôi: "Tôi nên tưới cây bao lâu một lần?" để nhận tư vấn.`,
        };
      }

      if (
        lowerMessage.includes("bệnh") ||
        lowerMessage.includes("vàng") ||
        lowerMessage.includes("héo")
      ) {
        return {
          content: `🔬 Để chẩn đoán bệnh trên cây chính xác, tôi cần xem hình ảnh của cây bạn.
          
          Khi chụp ảnh, hãy chú ý:
          • 📸 Chụp rõ nét phần lá bị bệnh
          • ☀️ Chụp dưới ánh sáng tự nhiên
          • 🔍 Bao gồm cả lá khỏe mạnh để so sánh
          • 📏 Chụp cả cây và cận cảnh vùng bị bệnh
          
          Upload hình ảnh để tôi phân tích nhé!`,
        };
      }

      return {
        content: `💬 Xin chào! Tôi là chatbot chuyên phân tích cây trồng.
        
        Tôi có thể giúp bạn:
        • 🌱 Nhận dạng loại cây từ hình ảnh
        • 🔬 Phát hiện bệnh và sâu hại
        • 📈 Đánh giá tình trạng sinh trưởng
        • 💡 Tư vấn cách chăm sóc
        • 📅 Tạo lịch chăm sóc cây
        
        Hãy gửi hình ảnh cây của bạn để tôi phân tích chi tiết!`,
      };
    },
    formatAnalysisText(analysisText) {
      if (!analysisText) return "";

      // Remove JSON markers and clean up
      let text = analysisText.replace(/```json|```/g, "").trim();

      // Try to parse as JSON first
      try {
        const jsonData = JSON.parse(text);
        return this.formatJsonAnalysis(jsonData);
      } catch (e) {
        // If not JSON, check if it's Vietnamese text
        if (text.includes("NHẬN DẠNG") || text.includes("TÌNH TRẠNG")) {
          return this.formatVietnameseText(text);
        }
        return text;
      }
    },

    formatVietnameseText(text) {
      // Format Vietnamese text with proper structure
      let formatted = text
        .replace(
          /(\d+\.\s*NHẬN DẠNG CÂY[^}]*})/g,
          "🔍 <strong>NHẬN DẠNG CÂY</strong><br>$1<br><br>"
        )
        .replace(
          /(\d+\.\s*TÌNH TRẠNG SỨC KHỎE[^}]*})/g,
          "⚕️ <strong>TÌNH TRẠNG SỨC KHỎE</strong><br>$1<br><br>"
        )
        .replace(
          /(\d+\.\s*PHÂN TÍCH SINH TRƯỞNG[^}]*})/g,
          "📈 <strong>PHÂN TÍCH SINH TRƯỞNG</strong><br>$1<br><br>"
        )
        .replace(
          /(\d+\.\s*KHUYẾN NGHỊ[^}]*})/g,
          "💡 <strong>KHUYẾN NGHỊ CHĂM SÓC</strong><br>$1<br><br>"
        )
        .replace(
          /(\d+\.\s*THÔNG TIN BỔ SUNG[^}]*})/g,
          "📋 <strong>THÔNG TIN BỔ SUNG</strong><br>$1<br><br>"
        );

      return formatted;
    },

    formatJsonAnalysis(data) {
      let formatted = "📊 <strong>Kết quả phân tích chi tiết:</strong><br><br>";

      for (const [key, value] of Object.entries(data)) {
        if (key.includes("NHẬN DẠNG") || key.includes("1.")) {
          formatted += "🔍 <strong>NHẬN DẠNG CÂY</strong><br>";
          formatted += this.formatPlantIdentification(value);
        } else if (key.includes("TÌNH TRẠNG") || key.includes("2.")) {
          formatted += "<br>⚕️ <strong>TÌNH TRẠNG SỨC KHỎE</strong><br>";
          formatted += this.formatHealthStatus(value);
        } else if (key.includes("SINH TRƯỞNG") || key.includes("3.")) {
          formatted += "<br>📈 <strong>PHÂN TÍCH SINH TRƯỞNG</strong><br>";
          formatted += this.formatGrowthAnalysis(value);
        } else if (key.includes("KHUYẾN NGHỊ") || key.includes("4.")) {
          formatted += "<br>💡 <strong>KHUYẾN NGHỊ CHĂM SÓC</strong><br>";
          formatted += this.formatRecommendations(value);
        } else if (key.includes("THÔNG TIN") || key.includes("5.")) {
          formatted += "<br>📋 <strong>THÔNG TIN BỔ SUNG</strong><br>";
          formatted += this.formatAdditionalInfo(value);
        }
      }

      return formatted;
    },

    formatPlantIdentification(data) {
      let result = "";
      
      // Handle different data structures
      if (!data || typeof data !== 'object') {
        return result;
      }
      
      // Check for nested name structure
      if (data["Tên khoa học và tên thông thường"]) {
        const names = data["Tên khoa học và tên thông thường"];
        if (typeof names === 'object') {
          result += `🏷️ <strong>Tên khoa học:</strong> ${
            names["Tên khoa học"] || "Chưa xác định"
          }<br>`;
          result += `🌿 <strong>Tên thông thường:</strong> ${
            names["Tên thông thường"] || "Chưa xác định"
          }<br>`;
        } else {
          // If names is a string, display it directly
          result += `🌿 <strong>Tên cây:</strong> ${names}<br>`;
        }
      }
      
      // Check for direct name fields
      if (data["Tên khoa học"]) {
        result += `🏷️ <strong>Tên khoa học:</strong> ${data["Tên khoa học"]}<br>`;
      }
      
      if (data["Tên thông thường"]) {
        result += `🌿 <strong>Tên thông thường:</strong> ${data["Tên thông thường"]}<br>`;
      }
      
      if (data["Họ thực vật"]) {
        result += `🌳 <strong>Họ thực vật:</strong> ${data["Họ thực vật"]}<br>`;
      }
      
      if (data["Độ tin cậy nhận dạng (%)"]) {
        result += `📊 <strong>Độ tin cậy:</strong> ${data["Độ tin cậy nhận dạng (%)"]}%<br>`;
      }
      
      // Handle confidence field variations
      if (data["confidence"]) {
        result += `📊 <strong>Độ tin cậy:</strong> ${data["confidence"]}%<br>`;
      }
      
      // If no specific fields found, try to display any text content
      if (!result) {
        for (const [key, value] of Object.entries(data)) {
          if (typeof value === 'string' && value.trim() && !key.includes(':')) {
            result += `🌿 <strong>${key}:</strong> ${value}<br>`;
          }
        }
      }
      
      return result;
    },

    formatHealthStatus(data) {
      let result = "";
      if (data["Tình trạng tổng thể"]) {
        const status = data["Tình trạng tổng thể"];
        const statusIcon =
          status === "Khỏe mạnh" ? "💚" : status === "Bệnh" ? "❤️‍🩹" : "⚠️";
        result += `${statusIcon} <strong>Trạng thái:</strong> ${status}<br>`;
      }
      if (data["Tên bệnh có thể"]) {
        result += `🦠 <strong>Bệnh:</strong> ${data["Tên bệnh có thể"]}<br>`;
      }
      if (data["Mức độ nghiêm trọng"]) {
        result += `⚖️ <strong>Mức độ:</strong> ${data["Mức độ nghiêm trọng"]}<br>`;
      }
      return result;
    },

    formatGrowthAnalysis(data) {
      let result = "";
      if (data["Giai đoạn phát triển"]) {
        result += `🌱 <strong>Giai đoạn:</strong> ${data["Giai đoạn phát triển"]}<br>`;
      }
      if (data["Tình trạng dinh dưỡng"]) {
        result += `🍃 <strong>Dinh dưỡng:</strong> ${data["Tình trạng dinh dưỡng"]}<br>`;
      }
      if (data["Tốc độ sinh trưởng"]) {
        result += `📈 <strong>Tốc độ phát triển:</strong> ${data["Tốc độ sinh trưởng"]}<br>`;
      }
      return result;
    },

    formatRecommendations(data) {
      let result = "";
      if (data["Biện pháp điều trị"]) {
        result += `💊 <strong>Điều trị:</strong><br>`;
        const treatment = data["Biện pháp điều trị"];
        if (typeof treatment === "object") {
          for (const [key, value] of Object.entries(treatment)) {
            result += `&nbsp;&nbsp;• ${value}<br>`;
          }
        } else {
          result += `&nbsp;&nbsp;• ${treatment}<br>`;
        }
      }
      if (data["Cách chăm sóc tối ưu"]) {
        result += `🌟 <strong>Chăm sóc:</strong><br>`;
        const care = data["Cách chăm sóc tối ưu"];
        if (typeof care === "object") {
          for (const [key, value] of Object.entries(care)) {
            result += `&nbsp;&nbsp;• ${value}<br>`;
          }
        } else {
          result += `&nbsp;&nbsp;• ${care}<br>`;
        }
      }
      return result;
    },

    formatAdditionalInfo(data) {
      let result = "";
      if (data["Nguồn gốc cây"]) {
        result += `🌍 <strong>Nguồn gốc:</strong> ${data["Nguồn gốc cây"]}<br>`;
      }
      if (data["Mùa sinh trưởng tốt nhất"]) {
        result += `🗓️ <strong>Mùa tốt nhất:</strong> ${data["Mùa sinh trưởng tốt nhất"]}<br>`;
      }
      if (data["Điều kiện trồng lý tưởng"]) {
        result += `🏡 <strong>Điều kiện lý tưởng:</strong><br>`;
        const conditions = data["Điều kiện trồng lý tưởng"];
        for (const [key, value] of Object.entries(conditions)) {
          result += `&nbsp;&nbsp;• ${key}: ${value}<br>`;
        }
      }
      return result;
    },

    formatJsonValue(value, indent = 0) {
      const indentStr = "&nbsp;".repeat(indent * 4);

      if (typeof value === "object" && value !== null) {
        let result = "";
        for (const [k, v] of Object.entries(value)) {
          result += `${indentStr}• <strong>${k}:</strong> `;
          if (typeof v === "object") {
            result += "<br>" + this.formatJsonValue(v, indent + 1);
          } else {
            result += `${v}<br>`;
          }
        }
        return result;
      }

      return `${indentStr}${value}<br>`;
    },

    formatTime(timestamp) {
      return timestamp.toLocaleTimeString("vi-VN", {
        hour: "2-digit",
        minute: "2-digit",
      });
    },

    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messagesContainer;
        if (container) {
          container.scrollTop = container.scrollHeight;
        }
      });
    },

    showError(message) {
      this.errorMessage = message;
      setTimeout(() => {
        this.errorMessage = "";
      }, 5000);
    },

    showSuccess(message) {
      this.successMessage = message;
      setTimeout(() => {
        this.successMessage = "";
      }, 3000);
    },

    clearMessages() {
      this.errorMessage = "";
      this.successMessage = "";
    },

    // Schedule Management Methods
    setDefaultStartDate() {
      const now = new Date();
      now.setMinutes(now.getMinutes() + 30); // 30 minutes from now
      this.newSchedule.startDate = now.toISOString().slice(0, 16);
    },

    loadSchedulesFromStorage() {
      const saved = localStorage.getItem("plantCareSchedules");
      if (saved) {
        try {
          const schedules = JSON.parse(saved);
          // Ensure all dates are properly parsed
          this.careSchedules = schedules.map(schedule => ({
            ...schedule,
            startDate: new Date(schedule.startDate),
            createdAt: schedule.createdAt ? new Date(schedule.createdAt) : new Date(),
            completedDates: schedule.completedDates ? 
              schedule.completedDates.map(date => new Date(date)) : []
          }));
          this.scheduleIdCounter =
            Math.max(...this.careSchedules.map((s) => s.id), 0) + 1;
        } catch (error) {
          console.error("Error loading schedules:", error);
          this.careSchedules = [];
          this.scheduleIdCounter = 1;
        }
      }
    },

    saveSchedulesToStorage() {
      localStorage.setItem(
        "plantCareSchedules",
        JSON.stringify(this.careSchedules)
      );
    },

    createSchedule() {
      if (!this.isScheduleValid) return;

      const schedule = {
        id: this.scheduleIdCounter++,
        plantName: this.newSchedule.plantName.trim(),
        careType: this.newSchedule.careType,
        startDate: new Date(this.newSchedule.startDate),
        repeatType: this.newSchedule.repeatType,
        repeatCount: parseInt(this.newSchedule.repeatCount) || 1,
        notes: this.newSchedule.notes.trim(),
        completedDates: [],
        createdAt: new Date(),
      };

      this.careSchedules.push(schedule);
      this.saveSchedulesToStorage();

      // Reset form
      this.newSchedule = {
        plantName: "",
        careType: "watering",
        startDate: "",
        repeatType: "none",
        repeatCount: 1,
        notes: "",
      };
      this.setDefaultStartDate();

      this.showScheduleModal = false;
      this.showSuccess(`Đã tạo lịch chăm sóc cho ${schedule.plantName}`);

      // Add bot message about schedule creation
      const botMessage = {
        id: this.messageId++,
        type: "bot",
        content: `✅ Đã tạo lịch chăm sóc thành công!
        
        📋 **${schedule.plantName}**
        ${this.getCareTypeIcon(schedule.careType)} ${this.getCareTypeName(
          schedule.careType
        )}
        ⏰ Bắt đầu: ${this.formatDateTime(schedule.startDate)}
        🔄 ${this.getRepeatText(schedule)}
        
        Tôi sẽ nhắc nhở bạn khi đến giờ chăm sóc!`,
        timestamp: new Date(),
      };
      this.messages.push(botMessage);
      this.scrollToBottom();
    },

    editSchedule(schedule) {
      // Ensure startDate is a Date object
      const startDate = schedule.startDate instanceof Date 
        ? schedule.startDate 
        : new Date(schedule.startDate);
      
      this.newSchedule = {
        plantName: schedule.plantName,
        careType: schedule.careType,
        startDate: startDate.toISOString().slice(0, 16),
        repeatType: schedule.repeatType,
        repeatCount: schedule.repeatCount,
        notes: schedule.notes,
      };
      this.newSchedule.editingId = schedule.id;
      this.showScheduleList = false;
      this.showScheduleModal = true;
    },

    deleteSchedule(scheduleId) {
      if (confirm("Bạn có chắc muốn xóa lịch chăm sóc này?")) {
        this.careSchedules = this.careSchedules.filter(
          (s) => s.id !== scheduleId
        );
        this.saveSchedulesToStorage();
        this.showSuccess("Đã xóa lịch chăm sóc");

        // Close details modal if this schedule was being viewed
        if (this.selectedSchedule && this.selectedSchedule.id === scheduleId) {
          this.showScheduleDetails = false;
          this.selectedSchedule = null;
        }
      }
    },

    // Schedule Details Methods
    viewScheduleDetails(schedule) {
      this.selectedSchedule = schedule;
      this.showScheduleDetails = true;
    },

    closeScheduleDetails() {
      this.showScheduleDetails = false;
      this.selectedSchedule = null;
    },

    duplicateSchedule(schedule) {
      const duplicatedSchedule = {
        ...schedule,
        id: this.scheduleIdCounter++,
        plantName: `${schedule.plantName} (Sao chép)`,
        startDate: new Date(),
        completedDates: [],
        createdAt: new Date(),
      };

      this.careSchedules.push(duplicatedSchedule);
      this.saveSchedulesToStorage();
      this.showSuccess(
        `Đã sao chép lịch chăm sóc cho ${duplicatedSchedule.plantName}`
      );
    },

    formatDateTime(date) {
      if (!date) return "";
      // Ensure we have a Date object
      const d = date instanceof Date ? date : new Date(date);
      // Check if date is valid
      if (isNaN(d.getTime())) return "Ngày không hợp lệ";
      
      return d.toLocaleString("vi-VN", {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    },

    getScheduleProgress(schedule) {
      if (!schedule.repeatCount || schedule.repeatCount === 1) {
        return schedule.completedDates.length > 0
          ? "Hoàn thành"
          : "Chưa thực hiện";
      }

      const completed = schedule.completedDates.length;
      const total = schedule.repeatCount;
      return `${completed}/${total} lần`;
    },

    getProgressPercentage(schedule) {
      if (!schedule.repeatCount || schedule.repeatCount === 1) {
        return schedule.completedDates.length > 0 ? 100 : 0;
      }

      const completed = schedule.completedDates.length;
      const total = schedule.repeatCount;
      return Math.min((completed / total) * 100, 100);
    },

    getNextReminder(schedule) {
      if (!schedule || schedule.repeatType === "none") return null;

      try {
        const lastCompleted =
          schedule.completedDates && schedule.completedDates.length > 0
            ? new Date(
                Math.max(
                  ...schedule.completedDates.map((d) => {
                    const date = d instanceof Date ? d : new Date(d);
                    return date.getTime();
                  })
                )
              )
            : null;

        const startDate = schedule.startDate instanceof Date 
          ? schedule.startDate 
          : new Date(schedule.startDate);
        
        const baseDate = lastCompleted || startDate;
        const nextDate = new Date(baseDate);

        switch (schedule.repeatType) {
          case "daily":
            nextDate.setDate(nextDate.getDate() + 1);
            break;
          case "weekly":
            nextDate.setDate(nextDate.getDate() + 7);
            break;
          case "monthly":
            nextDate.setMonth(nextDate.getMonth() + 1);
            break;
          default:
            return null;
        }

        // Check if we've reached the repeat limit
        if (
          schedule.repeatCount &&
          schedule.completedDates &&
          schedule.completedDates.length >= schedule.repeatCount
        ) {
          return null;
        }

        return nextDate;
      } catch (error) {
        console.error("Error calculating next reminder:", error);
        return null;
      }
    },

    markAsDone(scheduleId) {
      const schedule = this.careSchedules.find((s) => s.id === scheduleId);
      if (schedule) {
        const now = new Date();
        schedule.completedDates.push(now);
        this.saveSchedulesToStorage();
        this.showSuccess(
          `Đã hoàn thành: ${this.getCareTypeName(schedule.careType)}`
        );

        // Add bot message
        const botMessage = {
          id: this.messageId++,
          type: "bot",
          content: `🎉 Tuyệt vời! Bạn đã hoàn thành việc ${this.getCareTypeName(
            schedule.careType
          ).toLowerCase()} cho **${schedule.plantName}**.
          
          ${this.getEncouragementMessage(schedule.careType)}`,
          timestamp: new Date(),
        };
        this.messages.push(botMessage);
        this.scrollToBottom();
      }
    },

    getNextReminderDate(schedule) {
      const now = new Date();
      let nextDate = new Date(schedule.startDate);

      if (schedule.repeatType === "none") {
        return nextDate > now ? nextDate : null;
      }

      let count = 0;
      while (nextDate <= now && count < schedule.repeatCount) {
        switch (schedule.repeatType) {
          case "daily":
            nextDate.setDate(nextDate.getDate() + 1);
            break;
          case "weekly":
            nextDate.setDate(nextDate.getDate() + 7);
            break;
          case "monthly":
            nextDate.setMonth(nextDate.getMonth() + 1);
            break;
        }
        count++;
      }

      return count < schedule.repeatCount ? nextDate : null;
    },

    getCareTypeIcon(careType) {
      const icons = {
        watering: "💧",
        fertilizing: "🌱",
        pruning: "✂️",
        repotting: "🪴",
        spraying: "💨",
        checking: "🔍",
      };
      return icons[careType] || "🌿";
    },

    getCareTypeName(careType) {
      const names = {
        watering: "Tưới nước",
        fertilizing: "Bón phân",
        pruning: "Tỉa cành",
        repotting: "Thay chậu",
        spraying: "Phun thuốc",
        checking: "Kiểm tra sức khỏe",
      };
      return names[careType] || "Chăm sóc";
    },

    getRepeatText(schedule) {
      if (schedule.repeatType === "none") {
        return "Không lặp lại";
      }
      const typeNames = {
        daily: "hàng ngày",
        weekly: "hàng tuần",
        monthly: "hàng tháng",
      };
      return `Lặp lại ${typeNames[schedule.repeatType]} (${
        schedule.repeatCount
      } lần)`;
    },

    getEncouragementMessage(careType) {
      const messages = {
        watering: "💧 Cây sẽ rất khỏe mạnh với việc tưới nước đều đặn!",
        fertilizing: "🌱 Dinh dưỡng đầy đủ sẽ giúp cây phát triển mạnh mẽ!",
        pruning: "✂️ Việc tỉa cành giúp cây tập trung năng lượng phát triển!",
        repotting: "🪴 Không gian mới sẽ giúp rễ cây phát triển tốt hơn!",
        spraying: "💨 Cây được bảo vệ khỏi sâu bệnh rồi!",
        checking: "🔍 Theo dõi thường xuyên giúp phát hiện vấn đề sớm!",
      };
      return (
        messages[careType] ||
        "🌿 Việc chăm sóc đều đặn là chìa khóa thành công!"
      );
    },

    formatReminderTime(date) {
      const now = new Date();
      const diff = date - now;
      const minutes = Math.floor(diff / (1000 * 60));
      const hours = Math.floor(minutes / 60);

      if (minutes < 60) {
        return `${minutes} phút nữa`;
      } else if (hours < 24) {
        return `${hours} giờ nữa`;
      } else {
        return date.toLocaleDateString("vi-VN");
      }
    },

    setupReminderCheck() {
      // Check for reminders every minute
      this.reminderCheckInterval = setInterval(() => {
        this.checkUpcomingReminders();
      }, 60000);
    },

    checkUpcomingReminders() {
      const now = new Date();

      this.careSchedules.forEach((schedule) => {
        const nextDate = this.getNextReminderDate(schedule);
        if (nextDate) {
          const timeDiff = nextDate - now;

          // Remind 15 minutes before
          if (timeDiff > 0 && timeDiff <= 15 * 60 * 1000) {
            const lastNotified = localStorage.getItem(
              `notified_${schedule.id}`
            );
            const today = now.toDateString();

            if (lastNotified !== today) {
              this.showReminderNotification(schedule, nextDate);
              localStorage.setItem(`notified_${schedule.id}`, today);
            }
          }
        }
      });
    },

    showReminderNotification(schedule, nextDate) {
      const botMessage = {
        id: this.messageId++,
        type: "bot",
        content: `🔔 **Nhắc nhở chăm sóc cây!**
        
        ${this.getCareTypeIcon(schedule.careType)} **${schedule.plantName}**
        📅 ${this.getCareTypeName(schedule.careType)}
        ⏰ Trong ${this.formatReminderTime(nextDate)}
        
        ${schedule.notes ? `📝 ${schedule.notes}` : ""}
        
        Nhớ chăm sóc cây nhé! 🌿`,
        timestamp: new Date(),
      };

      this.messages.push(botMessage);
      this.scrollToBottom();

      // Browser notification if permitted
      if (Notification.permission === "granted") {
        new Notification(`Nhắc nhở chăm sóc: ${schedule.plantName}`, {
          body: `${this.getCareTypeName(
            schedule.careType
          )} trong ${this.formatReminderTime(nextDate)}`,
          icon: "/favicon.ico",
        });
      }
    },

    closeScheduleModal() {
      this.showScheduleModal = false;
      this.newSchedule = {
        plantName: "",
        careType: "watering",
        startDate: "",
        repeatType: "none",
        repeatCount: 1,
        notes: "",
      };
      this.setDefaultStartDate();
    },

    closeScheduleList() {
      this.showScheduleList = false;
    },

    // Extract plant information from AI analysis
    extractPlantInfo(analysisText, structuredData) {
      let plantInfo = {
        name: null,
        scientificName: null,
        commonName: null,
        plantType: null,
        healthStatus: null,
        careRequirements: {},
      };

      try {
        // Try to parse structured data first
        if (structuredData) {
          for (const [key, value] of Object.entries(structuredData)) {
            if (key.includes("NHẬN DẠNG") || key.includes("1.")) {
              if (value["Tên khoa học và tên thông thường"]) {
                const names = value["Tên khoa học và tên thông thường"];
                plantInfo.scientificName = names["Tên khoa học"] || null;
                plantInfo.commonName = names["Tên thông thường"] || null;
                plantInfo.name =
                  plantInfo.commonName ||
                  plantInfo.scientificName ||
                  "Cây không xác định";
              }
            } else if (key.includes("TÌNH TRẠNG") || key.includes("2.")) {
              plantInfo.healthStatus = value["Tình trạng tổng thể"] || null;
            } else if (key.includes("KHUYẾN NGHỊ") || key.includes("4.")) {
              plantInfo.careRequirements = value || {};
            }
          }
        }

        // If no structured data, try to extract from text
        if (!plantInfo.name && analysisText) {
          const nameMatch = analysisText.match(
            /(?:tên thông thường|common name)[:\s]*([^,\n]+)/i
          );
          if (nameMatch) {
            plantInfo.name = nameMatch[1].trim();
          }
        }

        // Set default name if still null
        if (!plantInfo.name) {
          plantInfo.name = "Cây trồng được phân tích";
        }
      } catch (error) {
        console.error("Error extracting plant info:", error);
        plantInfo.name = "Cây trồng được phân tích";
      }

      return plantInfo;
    },

    // Auto-generate care schedule based on AI analysis
    async autoGenerateCareSchedule(plantInfo, analysisData) {
      try {
        const careSchedules = this.generateCareRecommendations(
          plantInfo,
          analysisData
        );

        if (careSchedules.length > 0) {
          // Show confirmation dialog
          const confirmed = await this.showAutoScheduleConfirmation(
            plantInfo.name,
            careSchedules
          );

          if (confirmed) {
            // Create schedules
            careSchedules.forEach((schedule) => {
              this.createAutoSchedule(schedule);
            });

            // Show success message
            const botMessage = {
              id: this.messageId++,
              type: "bot",
              content: `🤖 **Tự động tạo lịch chăm sóc!**
              
              Tôi đã tự động tạo ${careSchedules.length} lịch chăm sóc cho **${
                plantInfo.name
              }** dựa trên kết quả phân tích:
              
              ${careSchedules
                .map(
                  (s) =>
                    `${this.getCareTypeIcon(s.careType)} ${this.getCareTypeName(
                      s.careType
                    )} - ${s.frequency}`
                )
                .join("\n")}
              
              Bạn có thể xem và chỉnh sửa trong mục "Xem lịch" ở sidebar! 📅`,
              timestamp: new Date(),
            };
            this.messages.push(botMessage);
            this.scrollToBottom();
          }
        }
      } catch (error) {
        console.error("Error generating auto schedule:", error);
      }
    },

    // Generate care recommendations based on plant type and health
    generateCareRecommendations(plantInfo, analysisData) {
      const schedules = [];
      const now = new Date();

      // Base watering schedule (most important)
      const wateringFrequency = this.determineWateringFrequency(plantInfo);
      schedules.push({
        plantName: plantInfo.name,
        careType: "watering",
        frequency: wateringFrequency.text,
        startDate: new Date(now.getTime() + 2 * 60 * 60 * 1000), // 2 hours from now
        repeatType: wateringFrequency.type,
        repeatCount: 30, // 1 month
        notes: `Lịch tưới tự động dựa trên phân tích AI. ${wateringFrequency.note}`,
        autoGenerated: true,
      });

      // Fertilizing schedule if plant is healthy or needs nutrients
      if (this.needsFertilizing(plantInfo, analysisData)) {
        schedules.push({
          plantName: plantInfo.name,
          careType: "fertilizing",
          frequency: "Hàng tuần",
          startDate: new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000), // 1 week from now
          repeatType: "weekly",
          repeatCount: 8, // 2 months
          notes: "Bón phân định kỳ để cây phát triển tốt hơn.",
          autoGenerated: true,
        });
      }

      // Health check schedule
      schedules.push({
        plantName: plantInfo.name,
        careType: "checking",
        frequency: "Hàng tuần",
        startDate: new Date(now.getTime() + 3 * 24 * 60 * 60 * 1000), // 3 days from now
        repeatType: "weekly",
        repeatCount: 12, // 3 months
        notes: "Kiểm tra tình trạng sức khỏe và phát hiện sớm các vấn đề.",
        autoGenerated: true,
      });

      // Disease treatment if unhealthy
      if (
        plantInfo.healthStatus &&
        plantInfo.healthStatus.toLowerCase().includes("bệnh")
      ) {
        schedules.push({
          plantName: plantInfo.name,
          careType: "spraying",
          frequency: "3 ngày một lần",
          startDate: new Date(now.getTime() + 12 * 60 * 60 * 1000), // 12 hours from now
          repeatType: "daily",
          repeatCount: 15, // Every 3 days for 45 days
          notes: "Phun thuốc điều trị bệnh theo khuyến nghị của AI.",
          autoGenerated: true,
        });
      }

      return schedules;
    },

    // Determine watering frequency based on plant type
    determineWateringFrequency(plantInfo) {
      const plantName = (plantInfo.name || "").toLowerCase();
      const scientificName = (plantInfo.scientificName || "").toLowerCase();

      // Different plant types have different watering needs
      if (
        plantName.includes("xương rồng") ||
        plantName.includes("cactus") ||
        scientificName.includes("cactaceae")
      ) {
        return {
          type: "weekly",
          text: "Hàng tuần",
          note: "Cây xương rồng cần ít nước, tưới 1 tuần/lần.",
        };
      } else if (
        plantName.includes("hoa hồng") ||
        scientificName.includes("rosa")
      ) {
        return {
          type: "daily",
          text: "2 ngày một lần",
          note: "Hoa hồng cần nước thường xuyên nhưng không quá ướt.",
        };
      } else if (plantName.includes("lan") || plantName.includes("orchid")) {
        return {
          type: "daily",
          text: "3 ngày một lần",
          note: "Lan cần độ ẩm vừa phải, tránh úng nước.",
        };
      } else if (plantName.includes("lá") || plantName.includes("cỏ")) {
        return {
          type: "daily",
          text: "Hàng ngày",
          note: "Cây lá xanh cần nước thường xuyên.",
        };
      } else {
        // Default for unknown plants
        return {
          type: "daily",
          text: "2 ngày một lần",
          note: "Lịch tưới tiêu chuẩn cho cây trồng thông thường.",
        };
      }
    },

    // Check if plant needs fertilizing
    needsFertilizing(plantInfo, analysisData) {
      // Check health status and growth analysis
      if (
        plantInfo.healthStatus &&
        plantInfo.healthStatus.toLowerCase().includes("khỏe mạnh")
      ) {
        return true; // Healthy plants benefit from regular fertilizing
      }

      // Check if analysis mentions nutrition issues
      if (analysisData) {
        const analysisText = JSON.stringify(analysisData).toLowerCase();
        if (
          analysisText.includes("dinh dưỡng") ||
          analysisText.includes("nutrition") ||
          analysisText.includes("phân bón") ||
          analysisText.includes("fertilizer")
        ) {
          return true;
        }
      }

      return true; // Default to fertilizing for most plants
    },

    // Show confirmation dialog for auto-generated schedules
    async showAutoScheduleConfirmation(plantName, schedules) {
      return new Promise((resolve) => {
        const message = `🤖 AI đề xuất tạo ${
          schedules.length
        } lịch chăm sóc cho "${plantName}":\n\n${schedules
          .map(
            (s) =>
              `${this.getCareTypeIcon(s.careType)} ${this.getCareTypeName(
                s.careType
              )} - ${s.frequency}`
          )
          .join("\n")}\n\nBạn có muốn tự động tạo các lịch này không?`;

        if (confirm(message)) {
          resolve(true);
        } else {
          resolve(false);
        }
      });
    },

    // Create auto-generated schedule
    createAutoSchedule(scheduleData) {
      const schedule = {
        id: this.scheduleIdCounter++,
        plantName: scheduleData.plantName,
        careType: scheduleData.careType,
        startDate: scheduleData.startDate,
        repeatType: scheduleData.repeatType,
        repeatCount: scheduleData.repeatCount,
        notes: scheduleData.notes,
        completedDates: [],
        createdAt: new Date(),
        autoGenerated: true, // Mark as auto-generated
      };

      this.careSchedules.push(schedule);
      this.saveSchedulesToStorage();
    },

    requestNotificationPermission() {
      if ("Notification" in window && Notification.permission === "default") {
        Notification.requestPermission().then((permission) => {
          if (permission === "granted") {
            this.showSuccess("Đã bật thông báo nhắc nhở chăm sóc cây!");
          }
        });
      }
    },
  },
};
</script>

<style scoped>
.chat-container {
  display: flex;
  height: 100vh;
  max-width: 1200px;
  margin: 0 auto;
  background: white;
  box-shadow: 0 0 50px rgba(0, 0, 0, 0.1);
}

.sidebar {
  width: 300px;
  background: #2c3e50;
  color: white;
  padding: 20px;
  overflow-y: auto;
}

.logo {
  text-align: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #34495e;
}

.logo h1 {
  font-size: 24px;
  color: #2ecc71;
  margin-bottom: 5px;
}

.logo p {
  font-size: 14px;
  color: #bdc3c7;
}

.chat-info {
  background: #34495e;
  padding: 15px;
  border-radius: 10px;
  margin-bottom: 20px;
}

.chat-info h3 {
  color: #2ecc71;
  margin-bottom: 10px;
  font-size: 16px;
}

.chat-info ul {
  list-style: none;
  font-size: 14px;
  line-height: 1.6;
}

.chat-info li {
  margin-bottom: 5px;
  color: #ecf0f1;
}

.chat-info li:before {
  content: "🌱 ";
  margin-right: 5px;
}

.main-chat {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #f8f9fa;
}

.chat-header {
  background: #2ecc71;
  color: white;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.chat-header h2 {
  font-size: 20px;
  margin-bottom: 5px;
}

.chat-header p {
  font-size: 14px;
  opacity: 0.9;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #ffffff;
}

.message {
  display: flex;
  margin-bottom: 20px;
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message.user {
  justify-content: flex-end;
}

.message.bot {
  justify-content: flex-start;
}

.message-content {
  max-width: 70%;
  padding: 15px 20px;
  border-radius: 20px;
  position: relative;
  word-wrap: break-word;
}

.message.user .message-content {
  background: #2ecc71;
  color: white;
  border-bottom-right-radius: 5px;
}

.message.bot .message-content {
  background: #ecf0f1;
  color: #2c3e50;
  border-bottom-left-radius: 5px;
}

.message-time {
  font-size: 12px;
  opacity: 0.7;
  margin-top: 5px;
}

.analysis-result {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 10px;
  padding: 15px;
  margin: 10px 0;
}

.analysis-section {
  margin-bottom: 15px;
}

.analysis-section h4 {
  color: #2ecc71;
  margin-bottom: 8px;
  font-size: 14px;
  display: flex;
  align-items: center;
}

.analysis-section h4 i {
  margin-right: 8px;
}

.analysis-section p,
.analysis-section li {
  font-size: 13px;
  line-height: 1.5;
  color: #495057;
}

.analysis-section ul {
  padding-left: 20px;
}

.image-preview img {
  max-width: 200px;
  border-radius: 10px;
  margin: 10px 0;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.chat-input-container {
  padding: 20px;
  background: white;
  border-top: 1px solid #dee2e6;
}

.chat-input-wrapper {
  display: flex;
  gap: 10px;
  align-items: flex-end;
}

.image-upload {
  position: relative;
}

.image-upload input[type="file"] {
  display: none;
}

.image-upload label {
  background: #f8f9fa;
  border: 2px dashed #dee2e6;
  border-radius: 10px;
  padding: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  transition: all 0.3s ease;
}

.image-upload label:hover {
  background: #e9ecef;
  border-color: #2ecc71;
}

.image-upload label.has-image {
  border-color: #2ecc71;
  background: #d4edda;
}

.image-upload label i {
  font-size: 20px;
  color: #6c757d;
}

.chat-input {
  flex: 1;
  padding: 15px 20px;
  border: 2px solid #dee2e6;
  border-radius: 25px;
  font-size: 16px;
  outline: none;
  transition: border-color 0.3s ease;
  resize: none;
  min-height: 60px;
  max-height: 120px;
}

.chat-input:focus {
  border-color: #2ecc71;
}

.send-button {
  background: #2ecc71;
  color: white;
  border: none;
  border-radius: 50%;
  width: 60px;
  height: 60px;
  cursor: pointer;
  transition: background 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.send-button:hover:not(:disabled) {
  background: #27ae60;
}

.send-button:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.send-button i {
  font-size: 20px;
}

.typing-indicator {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  background: #ecf0f1;
  border-radius: 20px;
  margin-bottom: 20px;
  max-width: 70%;
}

.typing-dots {
  display: flex;
  gap: 4px;
}

.typing-dots span {
  width: 8px;
  height: 8px;
  background: #95a5a6;
  border-radius: 50%;
  animation: typing 1.5s infinite ease-in-out;
}

.typing-dots span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%,
  60%,
  100% {
    transform: translateY(0);
    opacity: 0.5;
  }
  30% {
    transform: translateY(-10px);
    opacity: 1;
  }
}

.typing-text {
  margin-left: 10px;
  color: #7f8c8d;
  font-size: 14px;
}

.error-message {
  background: #e74c3c;
  color: white;
  padding: 10px 15px;
  border-radius: 10px;
  margin: 10px 0;
  font-size: 14px;
}

.success-message {
  background: #2ecc71;
  color: white;
  padding: 10px 15px;
  border-radius: 10px;
  margin: 10px 0;
  font-size: 14px;
}

@media (max-width: 768px) {
  .chat-container {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    height: auto;
    max-height: 200px;
  }

  .message-content {
    max-width: 85%;
  }
}

/* Schedule Management Styles */
.schedule-stats {
  font-size: 12px;
  color: #bdc3c7;
  margin-bottom: 15px;
}

.schedule-stats p {
  margin: 3px 0;
}

.create-schedule-btn,
.view-schedule-btn {
  background: #2ecc71;
  color: white;
  border: none;
  border-radius: 20px;
  padding: 8px 15px;
  cursor: pointer;
  font-size: 12px;
  margin: 5px 0;
  width: 100%;
  transition: all 0.3s ease;
}

.create-schedule-btn:hover,
.view-schedule-btn:hover {
  background: #27ae60;
  transform: translateY(-2px);
}

.create-schedule-btn i,
.view-schedule-btn i {
  margin-right: 5px;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 15px;
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  animation: modalSlideIn 0.3s ease-out;
}

.schedule-list-modal {
  max-width: 700px;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.modal-header {
  background: #2ecc71;
  color: white;
  padding: 20px;
  border-radius: 15px 15px 0 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 18px;
  cursor: pointer;
  padding: 5px;
  border-radius: 50%;
  transition: background 0.3s ease;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.modal-body {
  padding: 20px;
}

.modal-footer {
  padding: 20px;
  border-top: 1px solid #dee2e6;
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

/* Form Styles */
.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #2c3e50;
  font-size: 14px;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 12px;
  border: 2px solid #dee2e6;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #2ecc71;
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.btn-primary,
.btn-secondary {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.btn-primary {
  background: #2ecc71;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #27ae60;
}

.btn-primary:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
}

/* Schedule List Styles */
.schedule-tabs {
  display: flex;
  border-bottom: 1px solid #dee2e6;
  margin-bottom: 20px;
}

.tab-btn {
  background: none;
  border: none;
  padding: 12px 20px;
  cursor: pointer;
  color: #6c757d;
  border-bottom: 2px solid transparent;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.tab-btn.active {
  color: #2ecc71;
  border-bottom-color: #2ecc71;
}

.tab-btn:hover {
  color: #2ecc71;
}

.schedule-content {
  min-height: 300px;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #6c757d;
}

.empty-state i {
  font-size: 48px;
  margin-bottom: 16px;
  color: #dee2e6;
}

.empty-state p {
  margin-bottom: 20px;
}

/* Reminder and Schedule Items */
.reminder-item,
.schedule-item {
  display: flex;
  align-items: center;
  padding: 15px;
  border: 1px solid #dee2e6;
  border-radius: 10px;
  margin-bottom: 10px;
  transition: all 0.3s ease;
}

.reminder-item:hover,
.schedule-item:hover {
  border-color: #2ecc71;
  box-shadow: 0 2px 10px rgba(46, 204, 113, 0.1);
}

.reminder-item.urgent {
  border-color: #e74c3c;
  background: #fdf2f2;
}

.reminder-icon,
.schedule-icon {
  font-size: 24px;
  margin-right: 15px;
  width: 40px;
  text-align: center;
}

.reminder-info,
.schedule-info {
  flex: 1;
}

.reminder-info h4,
.schedule-info h4 {
  margin: 0 0 5px 0;
  color: #2c3e50;
  font-size: 16px;
}

.reminder-info p,
.schedule-info p {
  margin: 2px 0;
  color: #6c757d;
  font-size: 14px;
}

.reminder-time {
  color: #e74c3c;
  font-weight: bold;
  font-size: 12px;
}

.schedule-repeat {
  color: #2ecc71;
  font-size: 12px;
}

.schedule-notes {
  font-style: italic;
  color: #8b8b8b;
  font-size: 12px;
}

.auto-badge {
  display: inline-block;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 10px;
  margin-left: 8px;
  font-weight: normal;
  vertical-align: middle;
}

.done-btn {
  background: #2ecc71;
  color: white;
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.done-btn:hover {
  background: #27ae60;
  transform: scale(1.1);
}

.schedule-actions {
  display: flex;
  gap: 8px;
}

.edit-btn,
.delete-btn {
  background: none;
  border: 1px solid;
  border-radius: 6px;
  width: 32px;
  height: 32px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.edit-btn {
  border-color: #17a2b8;
  color: #17a2b8;
}

.edit-btn:hover {
  background: #17a2b8;
  color: white;
}

.delete-btn {
  border-color: #dc3545;
  color: #dc3545;
}

.delete-btn:hover {
  background: #dc3545;
  color: white;
}

/* Responsive Design */
@media (max-width: 768px) {
  .modal-content {
    margin: 10px;
    max-width: none;
  }

  .modal-header,
  .modal-body,
  .modal-footer {
    padding: 15px;
  }

  .reminder-item,
  .schedule-item {
    padding: 12px;
  }

  .form-group input,
  .form-group select,
  .form-group textarea {
    padding: 10px;
  }
}

/* Schedule Details Modal Styles */
.schedule-details-modal {
  max-width: 600px !important;
  max-height: 90vh;
  overflow-y: auto;
}

.schedule-detail-section {
  padding: 20px 0;
}

.detail-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 20px;
  padding: 15px;
  background: #f8fffe;
  border-radius: 10px;
  border: 1px solid #e0f0ef;
}

.detail-item label {
  font-weight: 600;
  color: #2c5530;
  min-width: 140px;
  margin-right: 15px;
  font-size: 14px;
}

.detail-value {
  flex: 1;
  color: #34495e;
  font-size: 14px;
  line-height: 1.5;
}

.notes-text {
  background: #fff;
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #ddd;
  font-style: italic;
}

.status-active {
  color: #27ae60;
  font-weight: 600;
  background: #d5f4e6;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.progress-info {
  flex: 1;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: #ecf0f1;
  border-radius: 4px;
  margin-top: 8px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #27ae60, #2ecc71);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.next-reminder {
  color: #e67e22;
  font-weight: 500;
}

.next-reminder small {
  display: block;
  color: #7f8c8d;
  font-size: 12px;
  margin-top: 4px;
}

.schedule-actions-detail {
  display: flex;
  gap: 10px;
  justify-content: center;
  padding: 20px 0;
  border-top: 1px solid #ecf0f1;
  margin-top: 20px;
}

.schedule-actions-detail button {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover {
  background: #2980b9;
  transform: translateY(-2px);
}

.btn-secondary {
  background: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background: #7f8c8d;
  transform: translateY(-2px);
}

.btn-danger {
  background: #e74c3c;
  color: white;
}

.btn-danger:hover {
  background: #c0392b;
  transform: translateY(-2px);
}

/* View button style */
.view-btn {
  background: #3498db;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 12px;
}

.view-btn:hover {
  background: #2980b9;
  transform: translateY(-1px);
}

.schedule-actions {
  display: flex;
  gap: 5px;
}
</style>
