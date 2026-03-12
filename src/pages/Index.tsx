import { useState } from "react";
import { useChatStore } from "@/hooks/useChatStore";
import { useTheme } from "@/hooks/useTheme";
import { useSettings } from "@/hooks/useSettings";
import { ChatSidebar } from "@/components/chat/ChatSidebar";
import { ChatArea } from "@/components/chat/ChatArea";
import { SettingsPanel } from "@/components/chat/SettingsPanel";

const Index = () => {
  const { theme, toggleTheme } = useTheme();
  const { settings, updateSettings, resetSettings } = useSettings();
  const {
    conversations,
    activeConversation,
    activeId,
    isGenerating,
    setActiveId,
    createConversation,
    deleteConversation,
    renameConversation,
    sendMessage,
  } = useChatStore(settings);

  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [settingsOpen, setSettingsOpen] = useState(false);

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <ChatSidebar
        conversations={conversations}
        activeId={activeId}
        onSelect={setActiveId}
        onCreate={createConversation}
        onDelete={deleteConversation}
        onRename={renameConversation}
        theme={theme}
        onToggleTheme={toggleTheme}
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        onOpenSettings={() => setSettingsOpen(true)}
      />
      <ChatArea
        conversation={activeConversation}
        isGenerating={isGenerating}
        onSend={sendMessage}
        onToggleSidebar={() => setSidebarOpen((p) => !p)}
        onOpenSettings={() => setSettingsOpen(true)}
        settings={settings}
      />
      <SettingsPanel
        open={settingsOpen}
        onClose={() => setSettingsOpen(false)}
        settings={settings}
        onUpdate={updateSettings}
        onReset={resetSettings}
      />
    </div>
  );
};

export default Index;
