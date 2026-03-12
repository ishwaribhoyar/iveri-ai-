import { X, RotateCcw, Volume2, VolumeX, Cpu, MessageSquareText, Sliders, Zap } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import type { Settings } from "@/types/chat";
import { AVAILABLE_MODELS, DEFAULT_SETTINGS } from "@/types/chat";

interface Props {
  open: boolean;
  onClose: () => void;
  settings: Settings;
  onUpdate: (partial: Partial<Settings>) => void;
  onReset: () => void;
}

export function SettingsPanel({ open, onClose, settings, onUpdate, onReset }: Props) {
  return (
    <AnimatePresence>
      {open && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-jarvis-deep/50 backdrop-blur-sm z-50"
            onClick={onClose}
          />
          <motion.div
            initial={{ opacity: 0, x: 80 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 80 }}
            transition={{ type: "spring", damping: 28, stiffness: 320 }}
            className="fixed right-0 top-0 bottom-0 w-full max-w-md bg-card border-l border-border z-50 flex flex-col shadow-2xl"
          >
            {/* Header */}
            <div className="flex items-center justify-between px-6 py-4 border-b border-border">
              <div className="flex items-center gap-2">
                <Sliders className="w-5 h-5 text-primary" />
                <h2 className="font-semibold text-lg text-card-foreground">Settings</h2>
              </div>
              <div className="flex items-center gap-1">
                <button
                  onClick={onReset}
                  className="p-2 rounded-lg text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors"
                  title="Reset to defaults"
                >
                  <RotateCcw className="w-4 h-4" />
                </button>
                <button
                  onClick={onClose}
                  className="p-2 rounded-lg text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Content */}
            <div className="flex-1 overflow-y-auto scrollbar-thin p-6 space-y-8">
              {/* Voice Section */}
              <section>
                <div className="flex items-center gap-2 mb-4">
                  {settings.voiceEnabled ? (
                    <Volume2 className="w-4 h-4 text-primary" />
                  ) : (
                    <VolumeX className="w-4 h-4 text-muted-foreground" />
                  )}
                  <h3 className="font-medium text-sm text-foreground">Voice</h3>
                </div>

                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-foreground">Voice Output</p>
                      <p className="text-xs text-muted-foreground">Speak AI responses aloud</p>
                    </div>
                    <button
                      onClick={() => onUpdate({ voiceEnabled: !settings.voiceEnabled })}
                      className={`relative w-11 h-6 rounded-full transition-colors ${
                        settings.voiceEnabled ? "bg-primary" : "bg-secondary"
                      }`}
                    >
                      <span
                        className={`absolute top-0.5 left-0.5 w-5 h-5 rounded-full bg-card shadow-sm transition-transform ${
                          settings.voiceEnabled ? "translate-x-5" : ""
                        }`}
                      />
                    </button>
                  </div>

                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <p className="text-sm text-foreground">Voice Speed</p>
                      <span className="text-xs text-muted-foreground font-mono">
                        {settings.voiceSpeed.toFixed(1)}x
                      </span>
                    </div>
                    <input
                      type="range"
                      min="0.5"
                      max="2.0"
                      step="0.1"
                      value={settings.voiceSpeed}
                      onChange={(e) => onUpdate({ voiceSpeed: parseFloat(e.target.value) })}
                      className="w-full accent-primary h-1.5 bg-secondary rounded-full appearance-none cursor-pointer"
                      disabled={!settings.voiceEnabled}
                    />
                    <div className="flex justify-between text-xs text-muted-foreground mt-1">
                      <span>0.5x</span>
                      <span>2.0x</span>
                    </div>
                  </div>
                </div>
              </section>

              {/* Model Section */}
              <section>
                <div className="flex items-center gap-2 mb-4">
                  <Cpu className="w-4 h-4 text-primary" />
                  <h3 className="font-medium text-sm text-foreground">Model</h3>
                </div>

                <div className="space-y-2">
                  {AVAILABLE_MODELS.map((model) => (
                    <button
                      key={model.id}
                      onClick={() => onUpdate({ model: model.id })}
                      className={`w-full text-left p-3 rounded-xl border transition-all ${
                        settings.model === model.id
                          ? "border-primary bg-primary/5 ring-1 ring-primary/20"
                          : "border-border hover:border-primary/30 hover:bg-secondary/50"
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <span className="text-sm font-medium text-foreground">{model.name}</span>
                        {settings.model === model.id && (
                          <span className="w-2 h-2 rounded-full bg-primary" />
                        )}
                      </div>
                      <p className="text-xs text-muted-foreground mt-0.5">{model.description}</p>
                    </button>
                  ))}
                </div>

                {/* Temperature */}
                <div className="mt-5">
                  <div className="flex items-center justify-between mb-2">
                    <p className="text-sm text-foreground">Temperature</p>
                    <span className="text-xs text-muted-foreground font-mono">
                      {settings.temperature.toFixed(1)}
                    </span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="2.0"
                    step="0.1"
                    value={settings.temperature}
                    onChange={(e) => onUpdate({ temperature: parseFloat(e.target.value) })}
                    className="w-full accent-primary h-1.5 bg-secondary rounded-full appearance-none cursor-pointer"
                  />
                  <div className="flex justify-between text-xs text-muted-foreground mt-1">
                    <span>Precise</span>
                    <span>Creative</span>
                  </div>
                </div>

                {/* Max Tokens */}
                <div className="mt-5">
                  <div className="flex items-center justify-between mb-2">
                    <p className="text-sm text-foreground">Max Tokens</p>
                    <span className="text-xs text-muted-foreground font-mono">
                      {settings.maxTokens}
                    </span>
                  </div>
                  <input
                    type="range"
                    min="256"
                    max="8192"
                    step="256"
                    value={settings.maxTokens}
                    onChange={(e) => onUpdate({ maxTokens: parseInt(e.target.value) })}
                    className="w-full accent-primary h-1.5 bg-secondary rounded-full appearance-none cursor-pointer"
                  />
                  <div className="flex justify-between text-xs text-muted-foreground mt-1">
                    <span>256</span>
                    <span>8192</span>
                  </div>
                </div>

                {/* Stream toggle */}
                <div className="flex items-center justify-between mt-5">
                  <div>
                    <div className="flex items-center gap-1.5">
                      <Zap className="w-3.5 h-3.5 text-primary" />
                      <p className="text-sm text-foreground">Stream Responses</p>
                    </div>
                    <p className="text-xs text-muted-foreground">Show tokens as they arrive</p>
                  </div>
                  <button
                    onClick={() => onUpdate({ streamResponses: !settings.streamResponses })}
                    className={`relative w-11 h-6 rounded-full transition-colors ${
                      settings.streamResponses ? "bg-primary" : "bg-secondary"
                    }`}
                  >
                    <span
                      className={`absolute top-0.5 left-0.5 w-5 h-5 rounded-full bg-card shadow-sm transition-transform ${
                        settings.streamResponses ? "translate-x-5" : ""
                      }`}
                    />
                  </button>
                </div>
              </section>

              {/* System Prompt Section */}
              <section>
                <div className="flex items-center gap-2 mb-4">
                  <MessageSquareText className="w-4 h-4 text-primary" />
                  <h3 className="font-medium text-sm text-foreground">System Prompt</h3>
                </div>

                <textarea
                  value={settings.systemPrompt}
                  onChange={(e) => onUpdate({ systemPrompt: e.target.value })}
                  rows={6}
                  className="w-full bg-secondary/50 border border-border rounded-xl px-4 py-3 text-sm text-foreground placeholder:text-muted-foreground outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary/50 resize-none scrollbar-thin transition-all"
                  placeholder="Define Jarvis's personality and behavior..."
                />
                <div className="flex items-center justify-between mt-2">
                  <p className="text-xs text-muted-foreground">
                    {settings.systemPrompt.length} characters
                  </p>
                  <button
                    onClick={() => onUpdate({ systemPrompt: DEFAULT_SETTINGS.systemPrompt })}
                    className="text-xs text-primary hover:underline"
                  >
                    Reset to default
                  </button>
                </div>
              </section>
            </div>

            {/* Footer */}
            <div className="px-6 py-4 border-t border-border bg-card/80">
              <p className="text-xs text-muted-foreground text-center">
                Settings are saved locally and apply to all conversations.
              </p>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
